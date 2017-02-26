import logging
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
NUM_OF_ARGS = 4

#   Display
SUCCESS_PRINT = '{style}{color}Success!'.format(
    style=Style.BRIGHT,
    color=Fore.GREEN,
)
FAILURE_PRINT = '{style}{color}Failed {hyphen}{message_color}'.format(
    style=Style.BRIGHT,
    color=Fore.RED,
    hyphen='{style}-'.format(style=Style.RESET_ALL),
    message_color=Fore.YELLOW,
)
DONE_PRINT = '{style}{color}Done!'.format(
    style=Style.BRIGHT,
    color=Fore.GREEN,
)

#   Logging
_HANDLER = colorlog.StreamHandler()
_HANDLER.setLevel(logging.INFO)
_HANDLER_FORMAT = '%(log_color)s%(asctime)s:%(name)s:%(levelname)s: %(message)s'  # noqa
_FORMATTER = colorlog.ColoredFormatter(_HANDLER_FORMAT,
                                       datefmt='%d/%m/%Y %H:%M:%S')
_HANDLER.setFormatter(_FORMATTER)

MAX_VERBOSITY = 3
VERBOSE_LEVELS = {
    0: logging.CRITICAL,
    1: logging.WARNING,
    2: logging.INFO,
    3: logging.DEBUG,
}
VERBOSITY_LEVEL = 0
MODULES_WITH_LOGGERS = (
    'screener.utils.decorators',
    'screener.utils.http_client',
    'screener.utils.images',
    'screener.utils.context_manager',
    'screener.core.screenshoting',
)


def init_logger(name):
    logger = colorlog.getLogger(name)
    _HANDLER.setLevel(VERBOSITY_LEVEL)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(_HANDLER)
    return logger
