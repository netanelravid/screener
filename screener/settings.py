from os import getcwd

import colorlog

#   Screenshoting
SCREENSHOT_WIDTH = 1366
SCREENSHOT_HEIGHT = 768

#   Other
CURRENT_DIR = getcwd()
VERSION = 0.3

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
    return logger
