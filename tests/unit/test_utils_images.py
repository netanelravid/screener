from os import path

import pytest

from screener.exceptions import DuplicateFile
from screener.utils.images import (
    save_as_jpg,
    IMAGE_EXT,
)
from tests.helpers import (
    get_resource,
    TEST_FILENAME,
)


@pytest.fixture(scope=u'module')
def test_image():
    return get_resource(u'test_image.png')


def test_save_as_jpg(tmpdir, test_image):
    folder = tmpdir.mkdir(u'screenshots').strpath
    save_as_jpg(image_date=test_image, folder=folder, filename=TEST_FILENAME)
    screenshot_filename = u'{fname}.{ext}'.format(
        fname=TEST_FILENAME, ext=IMAGE_EXT)
    file_path = path.join(folder, screenshot_filename)
    assert path.isfile(file_path)


def test_save_as_jpg_new_folder(tmpdir, test_image):
    folder = u'{dir}/new'.format(dir=tmpdir.mkdir(u'screenshots').strpath)
    assert not path.isdir(folder)
    save_as_jpg(image_date=test_image, folder=folder, filename=TEST_FILENAME)
    screenshot_filename = u'{fname}.{ext}'.format(
        fname=TEST_FILENAME, ext=IMAGE_EXT)
    file_path = path.join(folder, screenshot_filename)
    assert path.isfile(file_path)


@pytest.mark.parametrize(u'folder', [
    None, u'',
])
def test_save_as_jpg_invalid_folder(folder, test_image):
    with pytest.raises(IOError) as err:
        save_as_jpg(image_date=test_image, folder=folder, filename=u'test_1')
    assert err.value.message == u'Invalid folder'


def test_save_as_jpg_file_exist_error(tmpdir, test_image):
    folder = tmpdir.mkdir(u'screenshots').strpath
    screenshot_filename = u'{fname}.{ext}'.format(
        fname=TEST_FILENAME, ext=IMAGE_EXT)
    file_path = path.join(folder, screenshot_filename)
    with open(file_path, u'w') as fp:
        fp.write(u'test')
    assert path.isfile(file_path)
    with pytest.raises(DuplicateFile) as err:
        save_as_jpg(image_date=test_image,
                    folder=folder,
                    filename=TEST_FILENAME)
    assert err.value.message == u'File already exist'


@pytest.mark.parametrize(u'filename', [
    None, u'',
])
def test_save_as_jpg_invalid_filename(filename, tmpdir, test_image):
    folder = tmpdir.mkdir(u'screenshots').strpath
    with pytest.raises(IOError) as err:
        save_as_jpg(image_date=test_image, folder=folder, filename=filename)
    assert err.value.message == u'Invalid filename'


@pytest.mark.parametrize('image', [
    None, u'',
])
def test_save_as_jpg_invalid_image_data(tmpdir, image):
    folder = tmpdir.mkdir(u'screenshots').strpath
    with pytest.raises(IOError):
        save_as_jpg(image_date=image, folder=folder, filename=TEST_FILENAME)
