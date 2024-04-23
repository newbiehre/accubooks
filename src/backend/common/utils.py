import os
import re
from datetime import datetime


def get_date_year(date_str):
    try:
        parsed_date = datetime.strptime(str(date_str), '%d %b %Y')  # format "dd mm yyyy"
        return parsed_date.year
    except ValueError:
        return None


def remove_multiple_spaces(text: str):
    cleaned_string = None
    try:
        cleaned_string = re.sub(r'\s+', ' ', text)
    except Exception as e:
        raise ValueError(f"Cannot remove multiple spaces: {e}")
    finally:
        return cleaned_string


def format_amount(amount):
    return "{:.2f}".format(float(amount.replace(",", "")))


def convert_str_to_datetime(s: str) -> datetime:
    return datetime.strptime(s, "%d %b %Y")


def convert_to_datetime(input_datetime: datetime):
    return input_datetime.strftime("%d/%m/%Y")


def create_dir(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)
    return directory
