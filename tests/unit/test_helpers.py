import logging
import sys
from logging import (
    DEBUG,
    INFO,
    WARNING,
    CRITICAL,
    _loggerClass
)

import pytest
from future.backports.test.support import import_module

from screener.helpers import (
    screener_init,
    get_user_arguments,
    init_loggers,
)
from screener.settings import (
    init_logger,
    NUM_OF_ARGS,
    MODULES_WITH_LOGGERS,
)


@pytest.mark.parametrize('arguments, results', [
    (('', '-u', '123'),
     {'URL': '123',
      '--dir': 'Results',
      '--output': 'screenshot',
      '--verbose': 0}),
    (('', '-u', '123', '-v'),
     {'URL': '123',
      '--dir': 'Results',
      '--output': 'screenshot',
      '--verbose': 1}),
    (('', '-u', '123', '-vvv'),
     {'URL': '123',
      '--dir': 'Results',
      '--output': 'screenshot',
      '--verbose': 3}),
    (('', '-u', '123', '-d', 'temp_dir'),
     {'URL': '123',
      '--dir': 'temp_dir',
      '--output': 'screenshot',
      '--verbose': 0}),
    (('', '-u', '123', '--dir', 'temp_dir'),
     {'URL': '123',
      '--dir': 'temp_dir',
      '--output': 'screenshot',
      '--verbose': 0}),
    (('', '-u', '123', '-o', 'temp_image'),
     {'URL': '123',
      '--dir': 'Results',
      '--output': 'temp_image',
      '--verbose': 0}),
    (('', '-u', '123', '--output', 'temp_image'),
     {'URL': '123',
      '--dir': 'Results',
      '--output': 'temp_image',
      '--verbose': 0}),
    (('', '-u', '123', '-d', 'temp_dir', '-o', 'temp_image'),
     {'URL': '123',
      '--dir': 'temp_dir',
      '--output': 'temp_image',
      '--verbose': 0}),
])
def test_get_user_arguments(arguments, results):
    sys.argv = arguments
    args = get_user_arguments()
    args.pop('--url')
    assert args == results


def test_get_user_arguments_total_num():
    sys.argv = ('', '-u', '123')
    args = get_user_arguments()
    args.pop('--url')
    assert len(args) == NUM_OF_ARGS


def test_screener_init():
    #   Dump test, check that it runs without errors.
    screener_init()


def test_init_loggers():
    init_loggers(logging.INFO)

    modules_with_loggers = [import_module(module)
                            for module in MODULES_WITH_LOGGERS]
    for module in modules_with_loggers:
        assert isinstance(module.logger, _loggerClass)


@pytest.mark.parametrize('verbose_level, logging_level', [
    (0, CRITICAL),
    (1, WARNING),
    (2, INFO),
    (3, DEBUG),
])
def test_init_loggers_verbose_level(verbose_level, logging_level):
    init_loggers(verbose_level=verbose_level)
    test_logger = init_logger(__name__)
    assert test_logger.handlers[0].level == logging_level
