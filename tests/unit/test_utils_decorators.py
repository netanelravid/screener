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

FILE_EXT = u'txt'


@validate_path(ext=FILE_EXT)
def useless_func_validate_path(folder, filename):
    return True


@validate_path(ext=None)
def useless_func_validate_path_invalid_ext(folder, filename):
    return True


def test_validate_path(tmpdir):
    folder = tmpdir.mkdir(u'screenshots').strpath
    result = useless_func_validate_path(folder=folder, filename=u'test')
    assert result is True


@pytest.mark.parametrize(u'filename, folder, err_message', [
    (u'', u'', u'Invalid filename'),
    (None, u'', u'Invalid filename'),
    (u'test', u'', u'Invalid folder'),
    (u'test', None, u'Invalid folder'),
])
def test_validate_path_invalid(filename, folder, err_message):
    with pytest.raises(IOError) as err:
        useless_func_validate_path(folder=folder, filename=filename)
    assert err.value.message == err_message


def test_validate_path_invalid_ext():
    with pytest.raises(IOError) as err:
        useless_func_validate_path_invalid_ext(
            folder=u'test',
            filename=u'test_2'
        )
    assert err.value.message == u'Invalid file extension'


def test_validate_path_file_already_exist(tmpdir):
    folder = tmpdir.mkdir(u'screenshots').strpath
    filename = u'{name}.{ext}'.format(name=TEST_FILENAME, ext=FILE_EXT)
    file_path = path.join(folder, filename)
    with open(file_path, 'w') as fp:
        fp.write(u"I'm a new file")
    with pytest.raises(DuplicateFile) as err:
        useless_func_validate_path(folder=folder, filename=TEST_FILENAME)
    assert err.value.message == u'File already exist'


@validate_target
def useless_func_validate_target(url):
    return True


def test_validate_target(httpserver, example_site_source):
    httpserver.serve_content(example_site_source)
    result = useless_func_validate_target(url=httpserver.url)
    assert result is True


@pytest.mark.parametrize(u'status_code', [
    401, 403, 500, 503
])
def test_validate_target_bad_status_code(httpserver, status_code):
    httpserver.serve_content(u'Error', status_code)

    with pytest.raises(BadStatusCode) as err:
        useless_func_validate_target(url=httpserver.url)
    assert str(status_code) in err.value.message


@pytest.mark.parametrize(u'url, domain', [
    (None, u'None'),
    (u'', u''),
    (u'non valid site', u'non valid site'),
    (u'http://none', u'none'),
    (u'htta://asdasd', u'asdasd'),
    (u'http:none', u'none'),
])
def test_validate_target_invalid_url(url, domain):
    with pytest.raises(InvalidTargetException) as err:
        useless_func_validate_target(url=url)
    assert domain in err.value.message


@mock.patch(u'screener.utils.decorators.http_get_request')
def test_validate_target_timeout(get_mock):
    get_mock.side_effect = ConnectTimeout()
    with pytest.raises(ConnectionTimeout):
        useless_func_validate_target(url=u'http://test')


@mock.patch(u'screener.utils.decorators.http_get_request')
@pytest.mark.parametrize(u'exception, error_msg', [
    (KeyError, u'Key error'),
    (HTTPError, u'Good status code, this is absolutely an other error'),
    (ConnectionError, u'Good target, this is absolutely an other error'),
])
def test_validate_target_unknown_error(get_mock, exception, error_msg):
    get_mock.side_effect = exception(error_msg)
    with pytest.raises(UnknownError) as exc:
        useless_func_validate_target(url=u'http://none')
    assert exc.value.message == error_msg
