from colorama import (
    init,
    Fore,
    Style,
)
from docopt import docopt

from .settings import (
    VERSION,
    MAX_VERBOSITY,
    VERBOSE_LEVELS,
    init_logger
)


def _init_color_printing():
    init(autoreset=True)


def screener_init():
    _init_color_printing()
    _logo()


def _set_verbose_level(level):
    import settings
    level = MAX_VERBOSITY if level > MAX_VERBOSITY else level
    settings.VERBOSITY_LEVEL = VERBOSE_LEVELS[level]


def _logo():
    print('''
{style_1}{style_2}{color_2}------------------------------------------------------------------------------------------
{style_1}{style_2}{color_2}\                                                                          Ver. {VER}      /
{style_1}{style_1}{color_2} \    .oooooo..o    {color_5}                      Netanel.R.  {color_2}                                  /
{style_1}{style_2}{color_1}  |  d8P'    `Y8                                                                       |
{style_1}{style_3}{color_2} /   Y88bo.       .ooooo.  oooo d8b  .ooooo.   .ooooo.  ooo. .oo.    .ooooo.  oooo d8b  \\
{style_1}{style_3}{color_2}|     `"Y8888o.  d88' `"Y8 `888""8P d88' `88b d88' `88b `888P"Y88b  d88' `88b `888""8P   |
{style_1}{style_3}{color_3} \        `"Y88b 888        888     888ooo888 888ooo888  888   888  888ooo888  888      /
{style_1}{style_1}{color_3}  |  oo     .d8P 888   .o8  888     888    .o 888    .o  888   888  888    .o  888     |
{style_1}{style_2}{color_3} /   8""88888P'  `Y8bod8P' d888b    `Y8bod8P' `Y8bod8P' o888o o888o `Y8bod8P' d888b     \\
{style_1}{style_2}{color_4}/                                                                                        \\
{style_1}{style_2}{color_4}------------------------------------------------------------------------------------------
    '''.format(  # noqa
        color_1=Fore.LIGHTGREEN_EX,
        color_2=Fore.GREEN,
        color_3=Fore.WHITE,
        color_4=Fore.LIGHTBLACK_EX,
        color_5=Fore.RED,
        style_1=Style.RESET_ALL,
        style_2=Style.DIM,
        style_3=Style.BRIGHT,
        VER=VERSION,
    ))


def get_user_arguments():
    """
    Usage:
        screener.py --url URL [--dir=DIR] [--output=IMAGE] [--verbose...]

    Options:
        -u --url                    Targeted URL to screenshot.
        -d=DIR,--dir=DIR            Output folder name [default: Results]
        -o=IMAGE,--output=IMAGE     Output image name [default: screenshot]
        -h --help                   Show this screen.
        -v,--verbose                Verbosity level (-v, -vv, -vvv)
        --version                   Show version.

    Examples:
        screener.py -u http://www.github.com
        screener.py -u http://www.amazon.com -v
        screener.py -u http://www.ebay.com -vvv
        screener.py -u http://google.com -o google_website
        screener.py -u http://www.cnn.com -d my_screenshots
    """  # noqa
    docstring = get_user_arguments.__doc__
    arguments = docopt(
        doc=docstring,
        version='Screener V{ver}'.format(ver=VERSION)
    )
    return arguments


def init_loggers(verbose_level):
    from .utils import (
        decorators,
        http_client,
        images
    )

    _set_verbose_level(verbose_level)
    for lib in (decorators, http_client, images):
        lib.logger = init_logger(lib.LOGGER_NAME)
