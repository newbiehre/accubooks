import warnings

from src.backend.common.custom_logger import logger
from src.backend.global_variables import BASE_PATH, OUTPUT_PATH, FILE_PATH, HSBC_TEMPLATE_EXPENSE_DETAIL, \
    GENERATE_DEBUG_JSON
from src.frontend.gui_app import AccuBooksApp

if __name__ == "__main__":
    warnings.simplefilter(action='ignore', category=FutureWarning)

    try:
        logger.info(
            f"Global variables set (size: {len([BASE_PATH, OUTPUT_PATH, FILE_PATH,
                                                HSBC_TEMPLATE_EXPENSE_DETAIL, GENERATE_DEBUG_JSON])})")
        logger.info(f"Expense details to watch: (size: {HSBC_TEMPLATE_EXPENSE_DETAIL})")
        AccuBooksApp()
    except Exception as e:
        logger.critical(f"App cannot run ({e})")
        raise e
