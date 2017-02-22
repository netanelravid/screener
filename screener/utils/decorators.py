from functools import wraps
from os import makedirs
from os.path import isdir

from requests import (get as http_get_request)

from screener.exceptions import (
    BadTargetException,
    HTTP_ERRORS
)
from screener.settings import (
    SUCCESS_PRINT,
    FAILURE_PRINT,
    init_logger,
)

logger = init_logger(__name__)


def validate_path(wrapped):
    wraps(wrapped=wrapped)

    def inner(*args, **kwargs):
        filename = kwargs['filename']
        if not filename:
            raise IOError('Invalid filename')
        folder = kwargs['folder']
        if not folder:
            raise IOError('Invalid folder')
        if not isdir(folder):
            logger.warning('folder {dir} does not exist, creating it.'.format(
                dir=folder
            ))
            makedirs(folder)
        return wrapped(*args, **kwargs)
    return inner


def validate_target(wrapped):
    wraps(wrapped=wrapped)

    def inner(*args, **kwargs):
        url = kwargs['url']
        msg = 'Validate URL {url}\t'.format(url=url)
        logger.info(msg)
        print(msg),

        try:
            response = http_get_request(url=url)
            response.raise_for_status()
        except HTTP_ERRORS as e:
            logger.exception(e)
            print(FAILURE_PRINT + 'enable -v for verbosity')
            raise BadTargetException(msg=str(e.message))

        print(SUCCESS_PRINT)
        logger.info('URL has been validated successfully.')
        return wrapped(*args, **kwargs)
    return inner
