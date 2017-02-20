import pytest

from tests.helpers import get_resource


@pytest.fixture()
def example_site_source():
    return get_resource('example_com.html')
