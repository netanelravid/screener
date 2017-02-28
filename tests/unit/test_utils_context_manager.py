import logging
from testfixtures import log_capture

from screener.utils.context_manager import catch_keyboard_interrupt


@log_capture(u'screener.utils.context_manager', level=logging.WARNING)
def test_catch_keyboard_interrupt(logger_capture):
    with catch_keyboard_interrupt():
        raise KeyboardInterrupt()
    logger_capture.check(
        (u'screener.utils.context_manager',
         u'WARNING',
         u'Keyboard interrupt (CTRL-C)')
    )
