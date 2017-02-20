from functools import wraps
from os import makedirs
from os.path import isdir

from requests import (get as http_get_request)

from screener.exceptions import (
    BadTargetException,
    HTTP_ERRORS
)


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
            makedirs(folder)
        return wrapped(*args, **kwargs)
    return inner


def validate_target(wrapped):
    wraps(wrapped=wrapped)

    def inner(*args, **kwargs):
        url = kwargs['url']
        try:
            response = http_get_request(url=url)
            response.raise_for_status()
        except HTTP_ERRORS as e:
            raise BadTargetException(msg=str(e.message))
        return wrapped(*args, **kwargs)
    return inner
