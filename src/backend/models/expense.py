import re

from src.backend.models.enums import ExpenseCategory, MileageTypeCategory, PaidThroughCategory


def add_space_between_digit_and_space(text: str):
    for i, char in enumerate(text):
        if char.isalpha():
            return text[:i] + ' ' + text[i:]
    return text


def capitalize_all(text: str):
    text_list = remove_large_spaces(text).split(' ')
    capitalized_words = [item.capitalize() for item in text_list]
    return ",".join(capitalized_words).replace(",", " ").strip()


def remove_large_spaces(text: str):
    return re.sub(r'\s+', ' ', text)


class Expense:
    expense_date: str  # datetime
    merchant_name: str
    expense_description: str | None
    expense_category: ExpenseCategory
    currency_code: str
    exchange_rate: float | None
    mileage_rate: float
    distance: int
    expense_amount: str
    total: float
    receipt_id: str | None  # reference
    location: str
    is_reimbursable: bool
    start_odometer_reading: int
    end_odometer_reading: int
    is_billable: bool
    customer_name: str | None
    mileage_type: str | None
    paid_through: str | None

    def __init__(self, trans_date, year, currency_code, expense_amount, location, merchant_name,
                 expense_description=None, total=None, exchange_rate=None, mileage_rate=0, distance=0,
                 is_billable=False, mileage_type=MileageTypeCategory.NON_MILEAGE.value,
                 paid_through=PaidThroughCategory.CREDIT_CARD.value,
                 customer_name=None, start_odometer_reading=0, end_odometer_reading=0,
                 receipt_id=None, expense_category=ExpenseCategory.OTHER.value, is_reimbursable=True):
        f_trans_date = f"{add_space_between_digit_and_space(trans_date)} {year}"
        self.expense_date = f_trans_date  # convert_str_to_datetime(f_trans_date)
        self.merchant_name = capitalize_all(merchant_name)
        self.expense_description = expense_description
        self.expense_category = expense_category
        self.currency_code = currency_code
        self.exchange_rate = exchange_rate
        self.mileage_rate = mileage_rate
        self.distance = distance
        self.expense_amount = expense_amount
        self.total = total if total is not None else expense_amount
        self.receipt_id = receipt_id  # reference
        self.location = location
        self.is_reimbursable = is_reimbursable
        self.start_odometer_reading = start_odometer_reading
        self.end_odometer_reading = end_odometer_reading
        self.is_billable = is_billable
        self.customer_name = customer_name
        self.mileage_type = mileage_type
        self.paid_through = paid_through

    def shorter_version(self):
        return {
            'expense_date': self.expense_date,
            'merchant_name': self.merchant_name,
            'expense_amount': self.expense_amount,
            'location': self.location,
        }

    def __str__(self):
        return (f"\n\nExpense ("
                f"expense_date: {self.expense_date}, "
                f"expense_description: {self.expense_description}, "
                f"expense_category: {self.expense_category}, "
                f"\ncurrency_code: {self.currency_code}, "
                f"exchange_rate: {self.exchange_rate}, "
                f"mileage_rate: {self.mileage_rate}, "
                f"distance: {self.distance}, "
                f"total: {self.total}, "
                f"expense_amount: {self.expense_amount}, "
                f"\nreceipt_id: {self.receipt_id}, "
                f"location: {self.location}, "
                f"is_reimbursable: {self.is_reimbursable}, "
                f"merchant_name: {self.merchant_name}, "
                f"start_odometer_reading: {self.start_odometer_reading}, "
                f"\nend_odometer_reading: {self.end_odometer_reading}, "
                f"is_billable: {self.is_billable}, "
                f"customer_name: {self.customer_name}, "
                f"mileage_type: {self.mileage_type}, "
                f"paid_through: {self.paid_through}])")
