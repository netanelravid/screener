import os

from selenium.common.exceptions import WebDriverException
from selenium.webdriver import PhantomJS

from screener.exceptions import (
    CrawlerError,
    UnknownError,
)
from screener.settings import (
    SCREENSHOT_WIDTH,
    SCREENSHOT_HEIGHT,
)
from screener.utils.decorators import validate_target

PAGE_LOAD_TIMEOUT = 60
LOGS_PATH = os.devnull
PHANTOMJS_ERR = u"'phantomjs' executable needs to be in PATH."
PHANTOMJS__CUSTOM_ERR = u"Web driver exception (PhantomJS installed?), abort.."

logger = None
LOGGER_NAME = __name__


class Browser(object):
    __slots__ = ['name', '_driver', '_target_screenshot']

    def __init__(self):
        self.name = 'Screener'
        self._init_driver()
        self._target_screenshot = None
        self._driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        self._driver.set_window_size(width=SCREENSHOT_WIDTH,
                                     height=SCREENSHOT_HEIGHT)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug(u'Terminate PhantomJS webdriver..')
        self._driver.quit()

    def _init_driver(self):
        logger.debug(u'Init PhantomJS webdriver..')
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
    def _get(self, url):
        logger.info(u'Requesting {url}'.format(url=url))
        self._driver.get(url=url)
        self._target_screenshot = self._driver.get_screenshot_as_png()

    def get(self, url):
        self._target_screenshot = None
        try:
            self._get(url=url)
        except CrawlerError as e:
            if isinstance(e, UnknownError):
                logger.exception(e)
            else:
                logger.error(e.message)
            return False
        return True

    @property
    def target_screenshot(self):
        return self._target_screenshot
