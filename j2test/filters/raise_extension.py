#!/usr/bin/env python3

import typing as t

# Jinja2 causes some deprecation warning on import
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import jinja2.exceptions
    import jinja2.ext
    import jinja2.nodes
    import jinja2.parser


class RaiseExtension(jinja2.ext.Extension):
    """
    An extension for Jinja2, which implements the "raise" keyword.

    NOTE: The "raise" keyword can be used in the template code to throw
        an arbitrary message. The message will be wrapped in
        the TemplateRuntimeError exception. For example:

        {% raise "Something went wrong: %s" | format(vars.foo) %}
    """

    tags: t.ClassVar[t.Set[str]] = {"raise"}  # type: ignore
    """
    The set of keywords supported by this extension.
    """

    def parse(self, parser: jinja2.parser.Parser) -> jinja2.nodes.CallBlock:
        """
        Parses a single keyword supported by this extension.

        :param parser: The parser for the Jinja2 template stream
        :type parser: jinja2.parser.Parser

        :return: The CallBlock object, which throws the specified message
        :rtype: jinja2.nodes.CallBlock
        """

        # The parser is currently pointing to the extension keyword,
        # skip over it
        line = next(parser.stream).lineno

        # Parse the argument for "raise", which can be any expression
        message = parser.parse_expression()

        # This is effectively the {% call %} statement, which calls
        # _throw_message() as a macro
        return jinja2.nodes.CallBlock(
            self.call_method("_throw_message", [message], lineno=line),
            [],  # args
            [],  # defaults
            [],  # body
            lineno=line,
        )

    def _throw_message(self, message: str, caller: t.Any) -> None:
        """
        Throws the specified message wrapped in the TemplateRuntimeError
        exception.

        :param message: The message to throw
        :type message: str

        :param caller: The "caller" stream passed to the macro from {% call %}
        :type caller: Any

        :raises TemplateRuntimeError: The standard Jinja2 exception wrapping
                                    the specified message
        """
        raise jinja2.exceptions.TemplateRuntimeError(message)
