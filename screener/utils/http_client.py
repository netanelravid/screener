import os

from selenium.common.exceptions import WebDriverException
from selenium.webdriver import PhantomJS

from screener.exceptions import BadTargetException
from screener.settings import (
    SCREENSHOT_WIDTH,
    SCREENSHOT_HEIGHT,
    init_logger
)
from screener.utils.decorators import validate_target
from .images import save_as_jpg

PAGE_LOAD_TIMEOUT = 60
LOGS_PATH = os.devnull
logger = init_logger(__name__)
PHANTOMJS_ERR = "'phantomjs' executable needs to be in PATH."
PHANTOMJS__CUSTOM_ERR = "Web driver exception (PhantomJS installed??), abort.."


class Browser(object):
    __slots__ = ['name', '_driver']

    def __init__(self):
        self.name = 'Screener'
        self._init_driver()
        self._driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        self._driver.set_window_size(width=SCREENSHOT_WIDTH,
                                     height=SCREENSHOT_HEIGHT)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._driver.quit()

    def _init_driver(self):
        try:
            self._driver = PhantomJS(service_log_path=LOGS_PATH)
        except WebDriverException as e:
            if e.msg == PHANTOMJS_ERR:
                logger.error(PHANTOMJS__CUSTOM_ERR)
            raise e

    @property
    def page_source(self):
        return self._driver.page_source

    @validate_target
    def get(self, url):
        logger.info('Requesting {url}'.format(url=url))
        self._driver.get(url=url)

    def take_screenshot(self, url, folder, filename):
        try:
            self.get(url=url)
        except BadTargetException as exc:
            logger.error(exc.message)
            return
        png_data = self._driver.get_screenshot_as_png()
        save_as_jpg(image_date=png_data, folder=folder, filename=filename)
        log_msg = 'Saving image {name} for url {url}'.format(name=filename,
                                                             url=url)
        logger.info(log_msg)
