from os import getcwd

import colorlog
from colorama import (
    Style,
    Fore,
)

#   Screenshoting
SCREENSHOT_WIDTH = 1366
SCREENSHOT_HEIGHT = 768

#   Other
CURRENT_DIR = getcwd()
VERSION = 0.3

#   Display
COMMA_PRINT = Style.RESET_ALL + ', '
SUCCESS_PRINT = Style.BRIGHT + Fore.GREEN + 'Success!'
FAILURE_PRINT = Style.BRIGHT + Fore.RED + 'Failed' + COMMA_PRINT + Fore.YELLOW
DONE_PRINT = Style.BRIGHT + Fore.GREEN + 'Done'

#   Logging
_handler = colorlog.StreamHandler()
_logger_format = '%(log_color)s%(asctime)s:%(name)s:%(levelname)s: %(message)s'
_formatter = colorlog.ColoredFormatter(_logger_format,
                                       datefmt='%d/%m/%Y %H:%M:%S')
_handler.setFormatter(_formatter)
_logger_level = colorlog.colorlog.logging.DEBUG


def init_logger(name):
    logger = colorlog.getLogger(name)
    logger.setLevel(_logger_level)
    logger.addHandler(_handler)
    logger.disabled = False
    return logger
