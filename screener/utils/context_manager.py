from contextlib import contextmanager

from colorama import (
    Style,
    Fore,
)

logger = None
LOGGER_NAME = __name__


@contextmanager
def catch_keyboard_interrupt():
    try:
        yield
    except KeyboardInterrupt:
        logger.warning('Keyboard interrupt (CTRL-C)')
        print("{style}{color}CTRL-C pressed, abort..".format(
            style=Style.BRIGHT,
            color=Fore.YELLOW,
        ))
