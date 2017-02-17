import argparse

from screener.settings import CURRENT_DIR
from screener.utils.http_client import Browser

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='WebApp screenshoter!.')
    parser.add_argument('-url', help='URL to screenshot', required=True)
    parser.add_argument('-dir',
                        metavar='\b',
                        help='Directory to save screenshot',
                        default=CURRENT_DIR)
    parser.add_argument('-filename',
                        metavar='\b',
                        help='Screenshot filename',
                        default='screenshot')
    args = parser.parse_args()

    url = args.url
    browser = Browser()
    browser.take_screenshot(url=args.url,
                            folder=args.dir,
                            filename=args.filename)
