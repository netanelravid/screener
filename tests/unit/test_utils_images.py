from os import path

from screener.utils.images import (save_as_jpg, IMAGE_EXT)
from tests.helpers import get_resource


def test_save_as_jpg(tmpdir):
    image = get_resource('test_image.png')
    folder = tmpdir.mkdir('screenshots').strpath
    filename = 'test_screenshot'
    save_as_jpg(image_date=image, folder=folder, filename=filename)
    screenshot_filename = '{fname}.{ext}'.format(fname=filename, ext=IMAGE_EXT)
    file_path = path.join(folder, screenshot_filename)
    assert path.isfile(file_path)
