#!/usr/bin/env python3

import typing as t

# Jinja2 causes some deprecation warning on import
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import jinja2


class VeryStrictUndefined(jinja2.StrictUndefined):
    """
    An overload of StrictUndefined, which generates an exception
    the moment it is created without delaying the exception to the actual
    evaluation. This allows printing the error message even if
    and undefined referenced is passed to other filters, e.g. tojson.

    WARNING: Using this instead of StrictUndefined makes it impossible
            to use filters that detect undefined variables explicitly,
            e.g. "default". This is a necessary trade-off to get better
            error reporting for undefined variables.
    """

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        """
        The constructor override, which throws in construction.

        :param args: The positional arguments to the base class
        :type args: Any

        :param kwargs: The keywords arguments to the base class
        :type args: Any
        """

        # Initialize the base class first - this will make it possible
        # to use the same exception helper
        super().__init__(*args, **kwargs)
        self._fail_with_undefined_error()
