import pytest

from screener.exceptions import (
    InvalidTargetException,
    BadStatusCode,
    UnknownError,
    ConnectionTimeout,
    CrawlerError,
)


@pytest.mark.parametrize('exception', [
    InvalidTargetException, BadStatusCode, ConnectionTimeout, UnknownError
])
def test_bad_target_exception(exception):
    error_msg = 'error message'
    bad_target_exception = exception(msg=error_msg)
    assert isinstance(bad_target_exception, CrawlerError)
    assert error_msg in str(bad_target_exception)
