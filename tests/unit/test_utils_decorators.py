import mock
import pytest
from requests import ConnectTimeout

from screener.exceptions import BadTargetException
from screener.utils.decorators import (
    validate_path,
    validate_target,
)


@validate_path
def useless_func_validate_path(folder, filename):
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


@validate_target
def useless_func_validate_target(url):
    return True


def test_validate_target(httpserver, example_site_source):
    httpserver.serve_content(example_site_source)
    result = useless_func_validate_target(url=httpserver.url)
    assert result is True


@mock.patch('screener.utils.decorators.http_get_request')
def test_validate_target_invalid(get_mock):
    get_mock.side_effect = ConnectTimeout()
    with pytest.raises(BadTargetException):
        useless_func_validate_target(url='http://none')
