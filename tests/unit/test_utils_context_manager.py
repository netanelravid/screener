import logging
from testfixtures import log_capture

from screener.utils.context_manager import catch_keyboard_interrupt


@log_capture('screener.utils.context_manager', level=logging.WARNING)
def test_catch_keyboard_interrupt(logger_capture):
    with catch_keyboard_interrupt():
        raise KeyboardInterrupt()
    logger_capture.check(
        ('screener.utils.context_manager',
         'WARNING',
         'Keyboard interrupt (CTRL-C)')
    )
