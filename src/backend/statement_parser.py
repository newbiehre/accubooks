import csv
import json
import os.path
import platform

import fitz
import pandas as pd
import tabula

import src.backend.templates.hsbc_template as hsbc_headers
from src.backend.common.custom_logger import logger
from src.backend.common.utils import get_date_year, remove_multiple_spaces, format_amount, create_dir
from src.backend.global_variables import HSBC_TEMPLATE_EXPENSE_DETAIL, OUTPUT_PATH, GENERATE_DEBUG_JSON
from src.backend.models.expense import Expense


class StatementParser:
    _instance = None
    _is_initialized = False

    OUTPUT_PATH_CSV = create_dir(os.path.join(OUTPUT_PATH, "csv"))
    CURRENCY_CODE = "HKD"
    CITY = "Hong Kong"

    def __init__(self, file_path):
        self.year = None
        self.dfs = None
        self.file_name = None
        self.file_path = file_path
        self.key_value_pair = {"statement_date": None, "size": 0, "transactions": []}
        logger.debug(f"File path: {file_path}")

    def parse_statement(self):
        try:
            self.file_name = os.path.basename(self.file_path).removesuffix(".pdf")
            self._validate_statement_type()
            self.dfs = tabula.read_pdf(self.file_path, pages="all")
            self.year = self._find_statement_date()
            self._parse_dfs()
            self.key_value_pair["size"] = len(self.key_value_pair["transactions"])
            if GENERATE_DEBUG_JSON:
                self.generate_debug_json_file(OUTPUT_PATH, self.file_name, self.key_value_pair.copy())
        except Exception as e:
            logger.error(f'({self.file_name}) Importing statement error ({e.__class__.__name__}): {e}.')
            raise Exception(e)

    def export_csv_file(self):
        self.generate_csv_file(self.OUTPUT_PATH_CSV, self.file_name, self.key_value_pair["transactions"])

    def _validate_statement_type(self):
        doc = fitz.open(self.file_path)
        first_line = doc[0].get_text("text").split("\n")[0].strip()
        if first_line == 'Statement of HSBC EveryMile Credit Card Account':
            logger.info(f'({self.file_name}) Statement file is supported.')
        else:
            raise TypeError(f"Statement file is not supported")

    def _find_statement_date(self):
        yr = None
        for df in self.dfs:
            headers = df.columns.tolist()
            if yr is None and len(headers) == 3:
                date = headers[2].split("\r")[-1]
                self.key_value_pair["statement_date"] = date
                yr = get_date_year(date)
                logger.info(f'({self.file_name}) Extracted statement date and year ({date})')
        return yr

    def _parse_dfs(self):
        for df in self.dfs:
            headers = df.columns.tolist()
            match headers:
                case hsbc_headers.header_1:
                    self._retrieve_tx_without_r(df)
                case hsbc_headers.header_2:
                    self._retrieve_tx_with_r(df)
                case hsbc_headers.header_3:
                    pass
                case hsbc_headers.header_4:
                    for index, row in df.iterrows():
                        values = row.tolist()
                        first = values[0]
                        if pd.notna(first) and "\r" in first:
                            self._retrieve_tx_with_r(df)
                        else:
                            self._retrieve_tx_without_r(df)
                case _:
                    pass
        logger.info(f'({self.file_name}) Extracted all expense txs from dfs (size: {len(self.dfs)})')

    def _retrieve_tx_without_r(self, df):
        for index, row in df.iterrows():
            values = row.tolist()
            [_, trans_date, unfiltered_merchants, location, amount] = values

            if pd.notna(unfiltered_merchants) and any(keep_word in unfiltered_merchants for keep_word in
                                                      HSBC_TEMPLATE_EXPENSE_DETAIL):
                last_tx = self.key_value_pair["transactions"].pop()
                merchant_details = last_tx.merchant_name + "; " + unfiltered_merchants
                last_tx.merchant_name = merchant_details
                self.key_value_pair["transactions"].append(last_tx)
            else:
                if pd.notna(trans_date) and "CR" not in amount:
                    if len(values) == 5:
                        formatted_location = location[:-2] + " " + location[-2:]
                        merchant = unfiltered_merchants + " " + formatted_location
                        tx = Expense(
                            trans_date=trans_date,
                            year=self.year,
                            merchant_name=merchant,
                            currency_code=self.CURRENCY_CODE,
                            expense_amount=format_amount(amount),
                            location=self.CITY,
                        )
                        self.key_value_pair["transactions"].append(tx)

    def _retrieve_tx_with_r(self, df):
        df.dropna(inplace=True)
        values = []

        for index, row in df.iterrows():
            for item in row:
                data_list = item.split('\r')
                values.append(data_list)

        if values:
            [post_dates, trans_dates, unfiltered_merchants, amounts] = values
            size = len(post_dates)
            filtered_merchants = []

            for word in unfiltered_merchants:
                merchant = remove_multiple_spaces(word)
                if any(word in merchant for word in HSBC_TEMPLATE_EXPENSE_DETAIL):
                    if len(filtered_merchants) > 0:
                        prev_merch = filtered_merchants.pop()
                        modified_merch = prev_merch + "; " + merchant
                        filtered_merchants.append(modified_merch)
                    else:
                        prev_merch = self.key_value_pair["transactions"].pop()
                        logger.info(f"Using new df: filtered_merchants is empty. "
                                    f"Taking last df's last expense ({prev_merch.merchant_name})")
                        prev_merch.merchant_name = prev_merch.merchant_name + "; " + merchant
                        self.key_value_pair["transactions"].append(prev_merch)
                        logger.info(f"Replaced last df's last expense with new name ({prev_merch.merchant_name})")
                else:
                    filtered_merchants.append(merchant)

            if size != len(unfiltered_merchants):
                logger.warn(f"[_retrieve_tx_with_r] - check expenses "
                            f"from (date: {trans_dates[0]}, merchant: {filtered_merchants[0]}) "
                            f"to (date: {trans_dates[-1]}, merchant: {filtered_merchants[-1]})")

            for index in range(size):
                amount = amounts[index]
                if "CR" not in amount:
                    tx = Expense(
                        trans_date=trans_dates[index],
                        year=self.year,
                        merchant_name=filtered_merchants[index],
                        currency_code=self.CURRENCY_CODE,
                        expense_amount=format_amount(amount),
                        location=self.CITY,
                    )
                    self.key_value_pair["transactions"].append(tx)

    @classmethod
    def generate_csv_file(cls, path, file_name, expenses):
        new_file = os.path.join(path, f"{file_name}.csv")
        try:
            with open(new_file, mode="w", newline="") as file:
                fieldnames = ['Entry Number'] + list(Expense.__annotations__.keys())
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for i, expense in enumerate(expenses, start=1):
                    expense_dict = {'Entry Number': i}
                    expense_dict.update(expense.__dict__)
                    writer.writerow(expense_dict)
                file.close()
            logger.info(f"({file_name}) Generated csv file")
        except Exception as e:
            logger.error(f"({file_name}) Generated json debug file error ({e})")
            raise e

    @classmethod
    def generate_debug_json_file(cls, path, file_name, key_value_pair):
        reformatted_txs = [tx.shorter_version() for tx in key_value_pair["transactions"]]
        key_value_pair["transactions"] = reformatted_txs

        try:
            directory = create_dir(os.path.join(path, "debug"))
            new_file = os.path.join(directory, f"{file_name}.json")
            with open(new_file, "w") as json_file:
                json.dump(key_value_pair, json_file, indent=4)
                json_file.close()
            logger.info(f"({file_name}) Generated json debug file")
        except Exception as e:
            logger.error(f"({file_name}) Generated json debug file error ({e})")
            raise e

    @classmethod
    def open_exported_dir(cls):
        path = create_dir(cls.OUTPUT_PATH_CSV)

        system = platform.system()
        match system:
            case 'Windows':
                os.system(f'explorer "{path}"')
            case 'Darwin':
                os.system(f'open "{path}"')
            case 'Linux':
                os.system(f'xdg-open "{path}"')
            case _:
                logger.error(f"Unsupported operating system ({system})")
                raise SystemError("Unsupported operating system")
