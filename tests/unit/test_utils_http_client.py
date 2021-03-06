import logging

import mock
import pytest
from selenium.common.exceptions import WebDriverException
from testfixtures import (
    log_capture,
    LogCapture
)

from screener.exceptions import (
    InvalidTargetException,
    BadStatusCode,
    ConnectionTimeout,
    UnknownError,
)
from screener.utils.http_client import (
    Browser,
    PHANTOMJS_ERR,
    PHANTOMJS__CUSTOM_ERR,
)


@mock.patch('screener.utils.http_client.PhantomJS')
@log_capture('screener.utils.http_client', level=logging.ERROR)
def test_init_browser_invalid_webdriver(webdriver_mock, logger_capture):
    webdriver_mock.side_effect = WebDriverException(PHANTOMJS_ERR)
    with pytest.raises(WebDriverException):
        Browser()
    logger_capture.check(
        ('screener.utils.http_client',
         'ERROR',
         PHANTOMJS__CUSTOM_ERR),
    )


def test_get_request(httpserver, example_site_source):
    httpserver.serve_content(example_site_source)
    with Browser() as browser:
        assert browser.target_screenshot is None
        with LogCapture('screener.utils.http_client') as logger_capture:
            browser.get(url=httpserver.url)
        browser_clean_source_page = browser.page_source.replace('\n', '')
        example_site_clean_source_page = example_site_source.replace('\n', '')
        assert browser_clean_source_page == example_site_clean_source_page
        assert browser.target_screenshot is not None
    log_msg = 'Requesting {url}'.format(url=httpserver.url)
    logger_capture.check(
        ('screener.utils.http_client', 'INFO', log_msg),
    )


@mock.patch('screener.utils.http_client.Browser._get')
@pytest.mark.parametrize('exception, msg, exc_info', [
    (BadStatusCode, 'bad status code', False),
    (InvalidTargetException, 'invalid target', False),
    (ConnectionTimeout, 'connection timeout', False),
    (UnknownError, 'Unknown error, enable -v for more info', True),
])
def test_get_request_error(get_mock, exception, msg, exc_info, httpserver):
    with Browser() as browser:
        get_mock.side_effect = exception(msg=msg)
        with LogCapture('screener.utils.http_client', level=logging.ERROR)\
                as logger_capture:
            browser.get(url=httpserver.url)
        assert len(logger_capture.records) == 1
        assert msg in str(logger_capture.records[0].msg)
        assert bool(logger_capture.records[0].exc_info) is exc_info
