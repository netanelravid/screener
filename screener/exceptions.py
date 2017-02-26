from requests.exceptions import (
    InvalidSchema,
    MissingSchema,
    InvalidURL,
)

BAD_TARGET_ERRORS = (
    MissingSchema,
    InvalidSchema,
    InvalidURL,
)


class CrawlerError(BaseException):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return repr(self.message)


class InvalidTargetException(CrawlerError):
    """Raised when the target could not be achieved."""
    pass


class BadStatusCode(CrawlerError):
    """Raised when target response with bad status code."""
    pass


class ConnectionTimeout(CrawlerError):
    """Raised when the timeout limit has achieved."""
    pass


class UnknownError(CrawlerError):
    """
    Occurred when none of the known errors raised (for logging and
    Maintaining the code.
    """
    pass


class DuplicateFile(IOError):
    pass
