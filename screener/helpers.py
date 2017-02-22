import logging

from colorama import init
from docopt import docopt

from .settings import VERSION


def _init_color_printing():
    init(autoreset=True)


def screener_init():
    _init_color_printing()
    _set_verbose_level('')


def _set_verbose_level(level):
    logging.basicConfig(level=logging.disable(logging.CRITICAL))


def get_user_arguments():
    """
    Usage:
        screener.py (-u|--url) URL [-d=DIR|--dir=DIR] [-o=IMAGE|--output=IMAGE]

    Options:
        -u --url                    Targeted URL to screenshot.
        -d=DIR,--dir=DIR            Output folder name [default: Results]
        -o=IMAGE,--output=IMAGE     Output image name [default: screenshot]
        -h --help                   Show this screen.
        --version                   Show version.

    Examples:
        screener.py -u http://www.github.com
        screener.py -u http://google.com -o google_website
        screener.py -u http://www.cnn.com -d my_screenshots
    """
    docstring = get_user_arguments.__doc__
    arguments = docopt(
        doc=docstring,
        version='Screener V{ver}'.format(ver=VERSION)
    )
    return arguments
