from screener.exceptions import BadTargetException


def test_bad_target_exception():
    error_msg = 'error message'
    bad_target_exception = BadTargetException(msg=error_msg)
    assert error_msg in str(bad_target_exception)
