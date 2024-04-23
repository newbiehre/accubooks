import configparser
import os.path
import sys
from pathlib import Path

from src.backend.common.utils import create_dir
from src.config.config_builder import HSBC_TEMPLATE_SECTION, EXPENSE_DETAIL, DEBUG_SECTION, GENERATE_JSON

config = configparser.ConfigParser()


def validate_initialization():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
        output_path = create_dir(os.path.join(base_path, "accubooks-files/output"))
        print(f"Running as PyInstaller Bundle (base path: {base_path})")
    else:
        base_path = Path.cwd().parent
        output_path = create_dir(os.path.join(base_path, "files/output"))
        print(f"Running as a normal python process (base path: {base_path})")

    print(f"Output path: {output_path})")

    if getattr(sys, 'frozen', False):
        file_path = os.path.join(base_path, 'config.ini')
    else:
        file_path = os.path.join(base_path, 'src', 'config.ini')

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Cannot find file {file_path}. "
                                f"Please ensure config.ini is in the same directory as the main/.exe file.")
    else:
        config.read(file_path)

    return base_path, output_path, file_path


def get_hsbc_template_expense_details():
    return config.get(HSBC_TEMPLATE_SECTION, EXPENSE_DETAIL).split(",")


def generate_debug_json():
    return config.getboolean(DEBUG_SECTION, GENERATE_JSON)
