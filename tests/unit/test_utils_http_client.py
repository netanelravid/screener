from os import path

import pytest

from screener.utils.http_client import Browser
from screener.utils.images import IMAGE_EXT
from tests.helpers import get_resource


def test_take_screenshot(httpserver, tmpdir):
    folder = tmpdir.mkdir('screenshots').strpath
    filename = 'test_screenshot'
    page_source = get_resource('example_com.html')
    httpserver.serve_content(page_source)

    with Browser() as browser:
        browser.take_screenshot(url=httpserver.url,
                                folder=folder,
                                filename=filename)
    screenshot_filename = '{fname}.{ext}'.format(fname=filename, ext=IMAGE_EXT)
    file_path = path.join(folder, screenshot_filename)
    assert path.isfile(file_path)
