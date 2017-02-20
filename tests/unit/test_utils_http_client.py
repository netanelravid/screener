from os import path

import mock
import pytest
from requests import ConnectTimeout
from selenium.common.exceptions import WebDriverException
from testfixtures import (
    log_capture,
    LogCapture
)

from screener.exceptions import BadTargetException
from screener.utils.http_client import (
    Browser,
    PHANTOMJS_ERR,
    PHANTOMJS__CUSTOM_ERR
)
from screener.utils.images import IMAGE_EXT


def test_get_request(httpserver, example_site_source):
    httpserver.serve_content(example_site_source)
    with Browser() as browser:
        with LogCapture('screener.utils.http_client') as logger_capture:
            browser.get(url=httpserver.url)
        browser_clean_source_page = browser.page_source.replace('\n', '')
        example_site_clean_source_page = example_site_source.replace('\n', '')
        assert browser_clean_source_page == example_site_clean_source_page
    log_msg = 'Requesting {url}'.format(url=httpserver.url)
    logger_capture.check(
        ('screener.utils.http_client', 'INFO', log_msg),
    )


@pytest.mark.parametrize('status_code', [
    401, 403, 500, 503
])
def test_get_request_bad_status_code(httpserver, status_code):
    httpserver.serve_content('Error', status_code)

    with pytest.raises(BadTargetException) as err:
        with Browser() as browser:
            browser.get(url=httpserver.url)
    assert str(status_code) in err.value.message


@pytest.mark.parametrize('url, domain', [
    (None, 'None'),
    ('', ''),
    ('Invalid_url', 'Invalid_url'),
    ('http://none', 'none'),
])
def test_get_request_invalid_url(url, domain):
    with pytest.raises(BadTargetException) as err:
        with Browser() as browser:
            browser.get(url=url)
    assert domain in err.value.message


@mock.patch('screener.utils.decorators.http_get_request')
def test_get_request_timeout(get_mock):
    get_mock.side_effect = ConnectTimeout()
    with pytest.raises(BadTargetException):
        with Browser() as browser:
            browser.get(url='http://test')


def test_take_screenshot(httpserver, tmpdir, example_site_source):
    folder = tmpdir.mkdir('screenshots').strpath
    filename = 'test_screenshot'
    httpserver.serve_content(example_site_source)

    with LogCapture('screener.utils.http_client') as logger_capture:
        with Browser() as browser:
            browser.take_screenshot(
                url=httpserver.url,
                folder=folder,
                filename=filename
            )
    screenshot_filename = '{fname}.{ext}'.format(fname=filename, ext=IMAGE_EXT)
    file_path = path.join(folder, screenshot_filename)
    assert path.isfile(file_path)

    log_1_msg = 'Requesting {url}'.format(url=httpserver.url)
    log_2_msg = 'Saving image {name} for url {url}'.format(name=filename,
                                                           url=httpserver.url)
    logger_capture.check(
        ('screener.utils.http_client', 'INFO', log_1_msg),
        ('screener.utils.http_client', 'INFO', log_2_msg),
    )


@mock.patch('screener.utils.http_client.PhantomJS')
@log_capture('screener.utils.http_client')
def test_take_screenshot_invalid_webdriver(webdriver_mock, logger_capture):
    webdriver_mock.side_effect = WebDriverException(PHANTOMJS_ERR)
    with pytest.raises(WebDriverException):
        Browser()
    logger_capture.check(
        ('screener.utils.http_client',
         'ERROR',
         PHANTOMJS__CUSTOM_ERR),
    )


@mock.patch('screener.utils.http_client.Browser.get')
@log_capture('screener.utils.http_client')
def test_take_screenshot_http_error(browser_get_mock, logger_capture):
    err_msg = 'Error message'
    browser_get_mock.side_effect = BadTargetException(msg=err_msg)
    with Browser() as browser:
        browser.take_screenshot(url='http://test', folder='', filename='')
    logger_capture.check(
        ('screener.utils.http_client', 'ERROR', err_msg),
    )
