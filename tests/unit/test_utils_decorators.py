from os import path

import mock
import pytest
from requests import (
    ConnectTimeout,
    ConnectionError,
    HTTPError,
)

from screener.exceptions import (
    UnknownError,
    InvalidTargetException,
    BadStatusCode,
    ConnectionTimeout,
    DuplicateFile,
)
from screener.utils.decorators import (
    validate_path,
    validate_target,
)
from tests.helpers import TEST_FILENAME

FILE_EXT = 'txt'


@validate_path(ext=FILE_EXT)
def useless_func_validate_path(folder, filename):
    return True


@validate_path(ext=None)
def useless_func_validate_path_invalid_ext(folder, filename):
    return True


def test_validate_path(tmpdir):
    folder = tmpdir.mkdir('screenshots').strpath
    result = useless_func_validate_path(folder=folder, filename='test')
    assert result is True


@pytest.mark.parametrize('filename, folder, err_message', [
    ('', '', 'Invalid filename'),
    (None, '', 'Invalid filename'),
    ('test', '', 'Invalid folder'),
    ('test', None, 'Invalid folder'),
])
def test_validate_path_invalid(filename, folder, err_message):
    with pytest.raises(IOError) as err:
        useless_func_validate_path(folder=folder, filename=filename)
    assert err.value.message == err_message


def test_validate_path_invalid_ext():
    with pytest.raises(IOError) as err:
        useless_func_validate_path_invalid_ext(folder='test', filename='test2')
    assert err.value.message == 'Invalid file extension'


def test_validate_path_file_already_exist(tmpdir):
    folder = tmpdir.mkdir('screenshots').strpath
    filename = '{name}.{ext}'.format(name=TEST_FILENAME, ext=FILE_EXT)
    file_path = path.join(folder, filename)
    with open(file_path, 'w') as fp:
        fp.write("I'm a new file")
    with pytest.raises(DuplicateFile) as err:
        useless_func_validate_path(folder=folder, filename=TEST_FILENAME)
    assert err.value.message == 'File already exist'


@validate_target
def useless_func_validate_target(url):
    return True


def test_validate_target(httpserver, example_site_source):
    httpserver.serve_content(example_site_source)
    result = useless_func_validate_target(url=httpserver.url)
    assert result is True


@pytest.mark.parametrize('status_code', [
    401, 403, 500, 503
])
def test_validate_target_bad_status_code(httpserver, status_code):
    httpserver.serve_content('Error', status_code)

    with pytest.raises(BadStatusCode) as err:
        useless_func_validate_target(url=httpserver.url)
    assert str(status_code) in err.value.message


@pytest.mark.parametrize('url, domain', [
    (None, 'None'),
    ('', ''),
    ('non valid site', 'non valid site'),
    ('http://none', 'none'),
    ('htta://asdasd', 'asdasd'),
    ('http:none', 'none'),
])
def test_validate_target_invalid_url(url, domain):
    with pytest.raises(InvalidTargetException) as err:
        useless_func_validate_target(url=url)
    assert domain in err.value.message


@mock.patch('screener.utils.decorators.http_get_request')
def test_validate_target_timeout(get_mock):
    get_mock.side_effect = ConnectTimeout()
    with pytest.raises(ConnectionTimeout):
        useless_func_validate_target(url='http://test')


@mock.patch('screener.utils.decorators.http_get_request')
@pytest.mark.parametrize('exception, error_msg', [
    (KeyError, 'Key error'),
    (HTTPError, 'Good status code, this is absolutely an other error'),
    (ConnectionError, 'Good target, this is absolutely an other error'),
])
def test_validate_target_unknown_error(get_mock, exception, error_msg):
    get_mock.side_effect = exception(error_msg)
    with pytest.raises(UnknownError) as exc:
        useless_func_validate_target(url='http://none')
    assert exc.value.message == error_msg
