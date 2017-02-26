import logging
from os import path

import mock
from testfixtures import LogCapture

from screener.core.screenshoting import screenshot_single_target
from screener.exceptions import ConnectionTimeout
from screener.utils.http_client import Browser
from screener.utils.images import IMAGE_EXT
from tests.helpers import TEST_FILENAME


def test_screenshot_single_target(httpserver, tmpdir, example_site_source):
    folder = tmpdir.mkdir('screenshots').strpath
    httpserver.serve_content(example_site_source)

    with LogCapture('screener', level=logging.INFO) as logger_capture:
        with Browser() as browser:
            screenshot_single_target(
                browser=browser,
                url=httpserver.url,
                folder=folder,
                filename=TEST_FILENAME
            )
    assert browser.target_screenshot is not None
    screenshot_filename = '{fname}.{ext}'.format(
        fname=TEST_FILENAME,
        ext=IMAGE_EXT,
    )
    file_path = path.join(folder, screenshot_filename)
    assert path.isfile(file_path)

    logger_capture.check(
        ('screener.utils.decorators',
         'INFO',
         'Validate URL {url}\t'.format(url=httpserver.url)),
        ('screener.utils.decorators',
         'INFO',
         'URL has been validated successfully.'),
        ('screener.utils.http_client',
         'INFO',
         'Requesting {url}'.format(url=httpserver.url)),
        ('screener.core.screenshoting',
         'INFO',
         'Saving image for target {url}'.format(url=httpserver.url)),
        ('screener.core.screenshoting',
         'INFO',
         "Image '{name}' for url {url} saved successfully".format(
             name=TEST_FILENAME,
             url=httpserver.url,
         ))
    )


@mock.patch('screener.utils.decorators.http_get_request')
def test_screenshot_single_target_error(
        get_mock, httpserver, tmpdir, example_site_source):
    folder = tmpdir.mkdir('screenshots').strpath
    httpserver.serve_content(example_site_source)
    err_msg = 'Timeout'
    get_mock.side_effect = ConnectionTimeout(msg=err_msg)

    with LogCapture('screener', level=logging.INFO) as logger_capture:
        with Browser() as browser:
            screenshot_single_target(
                browser=browser,
                url=httpserver.url,
                folder=folder,
                filename=TEST_FILENAME
            )
    screenshot_filename = '{fname}.{ext}'.format(
        fname=TEST_FILENAME,
        ext=IMAGE_EXT,
    )
    file_path = path.join(folder, screenshot_filename)
    assert not path.isfile(file_path)
    assert browser.target_screenshot is None

    logger_capture.check(
        ('screener.utils.decorators',
         'INFO',
         'Validate URL {url}\t'.format(url=httpserver.url)),
        ('screener.utils.http_client', 'ERROR', 'Timeout'),
    )


def test_screenshot_single_target_capture_twice(
        httpserver, tmpdir, example_site_source):
    folder = tmpdir.mkdir('screenshots').strpath
    httpserver.serve_content(example_site_source)

    with Browser() as browser:
        screenshot_single_target(
            browser=browser,
            url=httpserver.url,
            folder=folder,
            filename=TEST_FILENAME
        )
    screenshot_filename = '{fname}.{ext}'.format(
        fname=TEST_FILENAME,
        ext=IMAGE_EXT,
    )
    file_path = path.join(folder, screenshot_filename)
    assert path.isfile(file_path)

    with LogCapture('screener', level=logging.INFO) as logger_capture:
        with Browser() as browser:
            screenshot_single_target(
                browser=browser,
                url=httpserver.url,
                folder=folder,
                filename=TEST_FILENAME
            )

    logger_capture.check(
        ('screener.utils.decorators',
         'INFO',
         'Validate URL {url}\t'.format(url=httpserver.url)),
        ('screener.utils.decorators',
         'INFO',
         'URL has been validated successfully.'),
        ('screener.utils.http_client',
         'INFO',
         'Requesting {url}'.format(url=httpserver.url)),
        ('screener.core.screenshoting',
         'INFO',
         'Saving image for target {url}'.format(url=httpserver.url)),
        ('screener.core.screenshoting',
         'WARNING',
         "Image '{name}.{ext}' already exist".format(
             name=TEST_FILENAME,
             ext=IMAGE_EXT
         ))
    )
