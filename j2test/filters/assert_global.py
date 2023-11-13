#!/usr/bin/env python3

import logging
from jinja2.utils import pass_context
from typing import Any

_logger = logging.getLogger(__name__)


@pass_context
def assert_func(context: Any, expression: bool, macro: str, fail_msg: str) -> None:
    if not expression:
        message = "ERROR: assertion failed: {}, macro: {}, filename: {}".format(fail_msg, macro, context.name)
        _logger.error(message)
        raise AssertionError(message)
