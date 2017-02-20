from os import path

import pytest

from screener.utils.images import (save_as_jpg, IMAGE_EXT)
from tests.helpers import get_resource

TEST_FILENAME = 'test_screenshot'


@pytest.fixture(scope='module')
def test_image():
    return get_resource('test_image.png')


def test_save_as_jpg(tmpdir, test_image):
    folder = tmpdir.mkdir('screenshots').strpath
    save_as_jpg(image_date=test_image, folder=folder, filename=TEST_FILENAME)
    screenshot_filename = '{fname}.{ext}'.format(
        fname=TEST_FILENAME, ext=IMAGE_EXT)
    file_path = path.join(folder, screenshot_filename)
    assert path.isfile(file_path)


def test_save_as_jpg_new_folder(tmpdir, test_image):
    folder = '{dir}/new'.format(dir=tmpdir.mkdir('screenshots').strpath)
    assert not path.isdir(folder)
    save_as_jpg(image_date=test_image, folder=folder, filename=TEST_FILENAME)
    screenshot_filename = '{fname}.{ext}'.format(
        fname=TEST_FILENAME, ext=IMAGE_EXT)
    file_path = path.join(folder, screenshot_filename)
    assert path.isfile(file_path)


@pytest.mark.parametrize('folder', [
    None, '',
])
def test_save_as_jpg_invalid_folder(folder, test_image):
    with pytest.raises(IOError) as err:
        save_as_jpg(image_date=test_image, folder=folder, filename='test_1')
    assert err.value.message == 'Invalid folder'


def test_save_as_jpg_file_exist_error(tmpdir, test_image):
    folder = tmpdir.mkdir('screenshots').strpath
    screenshot_filename = '{fname}.{ext}'.format(
        fname=TEST_FILENAME, ext=IMAGE_EXT)
    file_path = path.join(folder, screenshot_filename)
    with open(file_path, 'w') as fp:
        fp.write('test')
    assert path.isfile(file_path)
    with pytest.raises(IOError) as err:
        save_as_jpg(image_date=test_image,
                    folder=folder,
                    filename=TEST_FILENAME)
    assert err.value.message == 'File already exist'


@pytest.mark.parametrize('filename', [
    None, '',
])
def test_save_as_jpg_invalid_filename(filename, tmpdir, test_image):
    folder = tmpdir.mkdir('screenshots').strpath
    with pytest.raises(IOError) as err:
        save_as_jpg(image_date=test_image, folder=folder, filename=filename)
    assert err.value.message == 'Invalid filename'


@pytest.mark.parametrize('image', [
    None, '',
])
def test_save_as_jpg_invalid_image_data(tmpdir, image):
    folder = tmpdir.mkdir('screenshots').strpath
    with pytest.raises(IOError):
        save_as_jpg(image_date=image, folder=folder, filename=TEST_FILENAME)
