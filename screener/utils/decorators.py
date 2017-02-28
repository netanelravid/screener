from functools import wraps
from os import makedirs, path

from future.utils import raise_with_traceback
from requests import (
    get as http_get_request,
    HTTPError,
)
from requests.exceptions import (
    ConnectionError,
    ConnectTimeout
)

from screener.exceptions import (
    InvalidTargetException,
    BadStatusCode,
    BAD_TARGET_ERRORS,
    UnknownError,
    ConnectionTimeout,
    DuplicateFile,
    CrawlerError)
from screener.settings import (
    SUCCESS_PRINT,
    FAILURE_PRINT)

logger = None
LOGGER_NAME = __name__
CRAWLER_EXCEPTION_MESSAGE = {
    BadStatusCode: u'bad status code',
    InvalidTargetException: u'invalid target',
    ConnectionTimeout: u'connection timeout',
    UnknownError: u'Unknown error, enable -v for more info'
}
INVALID_TARGET_MESSAGE = u'Failed to establish a new connection'


def validate_path(*dec_args, **dec_kwargs):
    def outer(wrapped):
        wraps(wrapped=wrapped)

        def inner(*args, **kwargs):
            filename = kwargs[u'filename']
            if not filename:
                raise IOError(u'Invalid filename')
            file_ext = dec_kwargs[u'ext']
            if not file_ext:
                raise IOError(u'Invalid file extension')
            folder = kwargs[u'folder']
            if not folder:
                raise IOError(u'Invalid folder')
            filename_with_exit = u'{name}.{ext}'.format(
                name=filename,
                ext=file_ext
            )
            file_path = path.join(folder, filename_with_exit)
            if not path.isdir(folder):
                logger.warning(u'folder {dir} does not exist, creating it.'.format(  # noqa
                    dir=folder
                ))
                makedirs(folder)
            elif path.isfile(file_path):
                raise DuplicateFile(u'File already exist')
            return wrapped(*args, **kwargs)
        return inner
    return outer


def check_target(wrapped):
    wraps(wrapped=wrapped)

    def _check_bad_status_code(response, error_message):
        try:
            status_code = response.status_code
        except AttributeError:
            return
        if status_code and (400 <= status_code <= 600):
            raise BadStatusCode(msg=error_message)

    def _check_bad_target(exception, error_message):
        if (isinstance(exception, BAD_TARGET_ERRORS) or
            (isinstance(exception, ConnectionError) and (INVALID_TARGET_MESSAGE in error_message))):  # noqa
            raise InvalidTargetException(msg=error_message)

    def _check_target(url):
        response = None

        try:
            response = http_get_request(url=url)
            response.raise_for_status()
        except HTTPError as exc:
            error_msg = str(exc.message)
            _check_bad_status_code(response=response, error_message=error_msg)
            raise UnknownError(msg=error_msg)
        except ConnectTimeout:
            raise ConnectionTimeout(msg=u'Connection timeout')
        except (BAD_TARGET_ERRORS, ConnectionError) as exc:
            error_msg = str(exc.message)
            _check_bad_target(exception=exc, error_message=error_msg)
            raise UnknownError(msg=error_msg)
        except Exception as exc:
            raise_with_traceback(UnknownError(msg=str(exc.message)))

    def inner(*args, **kwargs):
        url = kwargs[u'url']
        msg = u'Validate URL {url}\t'.format(url=url)
        logger.info(msg)
        print(msg),

        try:
            _check_target(url=url)
        except CrawlerError as e:
            print(u'{failed} ({error})'.format(
                failed=FAILURE_PRINT,
                error=CRAWLER_EXCEPTION_MESSAGE[e.__class__]
            ))
            raise e

        print(SUCCESS_PRINT)
        logger.info(u'URL has been validated successfully.')
        return wrapped(*args, **kwargs)
    return inner
