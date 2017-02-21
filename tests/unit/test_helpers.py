import sys

import pytest

from screener.helpers import (
    screener_init,
    get_user_arguments,
)


@pytest.mark.parametrize('arguments, results', [
    (('', '-u', '123'),
     {'URL': '123', '--dir': 'Results', '--output': 'screenshot'}),
    (('', '-u', '123', '-d', 'temp_dir'),
     {'URL': '123', '--dir': 'temp_dir', '--output': 'screenshot'}),
    (('', '-u', '123', '--dir', 'temp_dir'),
     {'URL': '123', '--dir': 'temp_dir', '--output': 'screenshot'}),
    (('', '-u', '123', '-o', 'temp_image'),
     {'URL': '123', '--dir': 'Results', '--output': 'temp_image'}),
    (('', '-u', '123', '--output', 'temp_image'),
     {'URL': '123', '--dir': 'Results', '--output': 'temp_image'}),
    (('', '-u', '123', '-d', 'temp_dir', '-o', 'temp_image'),
     {'URL': '123', '--dir': 'temp_dir', '--output': 'temp_image'}),
])
def test_get_user_arguments(arguments, results):
    sys.argv = arguments
    args = get_user_arguments()
    args.pop('--url')
    assert args == results


def test_screener_init():
    #   Dump test, check that it runs without errors.
    screener_init()
