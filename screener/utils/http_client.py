import os

from selenium.webdriver import PhantomJS

from screener.settings import (
    SCREENSHOT_WIDTH,
    SCREENSHOT_HEIGHT
)
from .images import save_as_jpg

PAGE_LOAD_TIMEOUT = 60
LOGS_PATH = os.devnull


class Browser(object):
    __slots__ = ['name', '_driver']

    def __init__(self):
        self.name = 'Screener'
        self._driver = PhantomJS(service_log_path=LOGS_PATH)
        self._driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        self._driver.set_window_size(width=SCREENSHOT_WIDTH,
                                     height=SCREENSHOT_HEIGHT)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._driver.quit()

    def _get(self, url):
        self._driver.get(url=url)

    def take_screenshot(self, url, folder, filename):
        self._get(url=url)
        png_data = self._driver.get_screenshot_as_png()
        save_as_jpg(image_date=png_data, folder=folder, filename=filename)
