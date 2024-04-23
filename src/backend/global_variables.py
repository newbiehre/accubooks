from src.config.config_reader import validate_initialization, get_hsbc_template_expense_details, generate_debug_json

BASE_PATH, OUTPUT_PATH, FILE_PATH = validate_initialization()
HSBC_TEMPLATE_EXPENSE_DETAIL = get_hsbc_template_expense_details()
GENERATE_DEBUG_JSON = generate_debug_json()
