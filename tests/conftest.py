import logging
import pytest

from tests.helpers import get_resource


@pytest.fixture()
def example_site_source():
    return get_resource('example_com.html')


@pytest.fixture(autouse=True)
def enable_loggers():
    logging.basicConfig(level=logging.disable(logging.NOTSET))
