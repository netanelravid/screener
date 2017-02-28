import pytest

from screener.helpers import init_loggers
from screener.settings import MAX_VERBOSITY
from tests.helpers import get_resource


@pytest.fixture()
def example_site_source():
    return get_resource(u'example_com.html')


@pytest.fixture(autouse=True)
def enable_loggers():
    init_loggers(verbose_level=MAX_VERBOSITY)
