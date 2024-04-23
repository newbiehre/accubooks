import configparser

config = configparser.ConfigParser()

HSBC_TEMPLATE_SECTION = "HSBC_TEMPLATE"
EXPENSE_DETAIL = "EXPENSE_DETAIL"
DEBUG_SECTION = "DEBUG"
GENERATE_JSON = "GENERATE_JSON"


def create_config_ini():
    config.add_section(HSBC_TEMPLATE_SECTION)
    config.set(HSBC_TEMPLATE_SECTION, EXPENSE_DETAIL, 'APPLE PAY-, CRI:, EXCHANGE RATE')

    config.add_section(DEBUG_SECTION)
    config.set(DEBUG_SECTION, GENERATE_JSON, 'True')
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
