from screener.helpers import (
    get_user_arguments,
    screener_init,
)
from screener.utils.http_client import Browser

if __name__ == '__main__':
    screener_init()
    args = get_user_arguments()

    with Browser() as browser:
        browser.take_screenshot(
            url=args['URL'],
            folder=args['--dir'],
            filename=args['--output']
        )
