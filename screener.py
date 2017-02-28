from screener.core.screenshoting import screenshot_single_target
from screener.helpers import (
    get_user_arguments,
    screener_init,
    init_loggers,
)
from screener.utils.context_manager import catch_keyboard_interrupt
from screener.utils.http_client import Browser

if __name__ == '__main__':
    screener_init()
    args = get_user_arguments()
    init_loggers(verbose_level=args[u'--verbose'])

    with catch_keyboard_interrupt():
        with Browser() as browser:
            screenshot_single_target(
                browser=browser,
                url=args[u'URL'],
                folder=args[u'--dir'],
                filename=args[u'--output']
            )
