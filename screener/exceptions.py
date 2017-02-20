from requests import HTTPError
from requests.exceptions import (
    MissingSchema,
    ConnectionError,
    ConnectTimeout as RequestsConnectTimeout,
)

HTTP_ERRORS = (
    HTTPError,
    MissingSchema,
    ConnectionError,
    RequestsConnectTimeout,
)


class BrowserError(BaseException):
    pass


class BadTargetException(BrowserError):
    """When a HTTP request cause one of the following:
    Timeout in response,
    Bad status code,
    Invalid URL,
    Connection error.
    """
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return repr(self.message)
