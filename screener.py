from screener.helpers import (
    get_user_arguments,
    screener_init,
    init_loggers,
)
from screener.utils.http_client import Browser

if __name__ == '__main__':
    screener_init()
    args = get_user_arguments()
    init_loggers(verbose_level=args['--verbose'])

    with Browser() as browser:
        browser.take_screenshot(
            url=args['URL'],
            folder=args['--dir'],
            filename=args['--output']
        )
