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
    folder = tmpdir.mkdir(u'screenshots').strpath
    httpserver.serve_content(example_site_source)

    with LogCapture(u'screener', level=logging.INFO) as logger_capture:
        with Browser() as browser:
            screenshot_single_target(
                browser=browser,
                url=httpserver.url,
                folder=folder,
                filename=TEST_FILENAME
            )
    assert browser.target_screenshot is not None
    screenshot_filename = u'{fname}.{ext}'.format(
        fname=TEST_FILENAME,
        ext=IMAGE_EXT,
    )
    file_path = path.join(folder, screenshot_filename)
    assert path.isfile(file_path)

    logger_capture.check(
        (u'screener.utils.decorators',
         u'INFO',
         u'Validate URL {url}\t'.format(url=httpserver.url)),
        (u'screener.utils.decorators',
         u'INFO',
         u'URL has been validated successfully.'),
        (u'screener.utils.http_client',
         u'INFO',
         u'Requesting {url}'.format(url=httpserver.url)),
        (u'screener.core.screenshoting',
         u'INFO',
         u'Saving image for target {url}'.format(url=httpserver.url)),
        (u'screener.core.screenshoting',
         u'INFO',
         u"Image '{name}' for url {url} saved successfully".format(
             name=TEST_FILENAME,
             url=httpserver.url,
         ))
    )


@mock.patch(u'screener.utils.decorators.http_get_request')
def test_screenshot_single_target_error(
        get_mock, httpserver, tmpdir, example_site_source):
    folder = tmpdir.mkdir(u'screenshots').strpath
    httpserver.serve_content(example_site_source)
    err_msg = u'Timeout'
    get_mock.side_effect = ConnectionTimeout(msg=err_msg)

    with LogCapture(u'screener', level=logging.INFO) as logger_capture:
        with Browser() as browser:
            screenshot_single_target(
                browser=browser,
                url=httpserver.url,
                folder=folder,
                filename=TEST_FILENAME
            )
    screenshot_filename = u'{fname}.{ext}'.format(
        fname=TEST_FILENAME,
        ext=IMAGE_EXT,
    )
    file_path = path.join(folder, screenshot_filename)
    assert not path.isfile(file_path)
    assert browser.target_screenshot is None

    logger_capture.check(
        (u'screener.utils.decorators',
         u'INFO',
         u'Validate URL {url}\t'.format(url=httpserver.url)),
        (u'screener.utils.http_client', u'ERROR', u'Timeout'),
    )


def test_screenshot_single_target_capture_twice(
        httpserver, tmpdir, example_site_source):
    folder = tmpdir.mkdir(u'screenshots').strpath
    httpserver.serve_content(example_site_source)

    with Browser() as browser:
        screenshot_single_target(
            browser=browser,
            url=httpserver.url,
            folder=folder,
            filename=TEST_FILENAME
        )
    screenshot_filename = u'{fname}.{ext}'.format(
        fname=TEST_FILENAME,
        ext=IMAGE_EXT,
    )
    file_path = path.join(folder, screenshot_filename)
    assert path.isfile(file_path)

    with LogCapture(u'screener', level=logging.INFO) as logger_capture:
        with Browser() as browser:
            screenshot_single_target(
                browser=browser,
                url=httpserver.url,
                folder=folder,
                filename=TEST_FILENAME
            )

    logger_capture.check(
        (u'screener.utils.decorators',
         u'INFO',
         u'Validate URL {url}\t'.format(url=httpserver.url)),
        (u'screener.utils.decorators',
         u'INFO',
         u'URL has been validated successfully.'),
        (u'screener.utils.http_client',
         u'INFO',
         u'Requesting {url}'.format(url=httpserver.url)),
        (u'screener.core.screenshoting',
         u'INFO',
         u'Saving image for target {url}'.format(url=httpserver.url)),
        (u'screener.core.screenshoting',
         u'WARNING',
         u"Image '{name}.{ext}' already exist".format(
             name=TEST_FILENAME,
             ext=IMAGE_EXT
         ))
    )
