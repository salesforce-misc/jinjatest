#!/usr/bin/env python3

import typing as t
import rapidjson as json


def simple_to_json_filter(
    value: t.Any,
    indent: t.Optional[int] = None,
    sort_keys: bool = True,
) -> str:
    """
    A wrapper around json.dumps(), which exposes only indent and sort_keys
    arguments.

    NOTE: This function is meant to be used as a replacement for
        the standard Jinja2 "tojson" filter. This replacement is required
        because the standard "tojson" filter performs HTML character escaping
        (for characters like <, > etc.), which is not required
        (and dangerous) if the Jinja2 template is used to produce a pure
        JSON output.

    :param value: The value to serialize to JSON
    :type value: Any

    :param indent: If specified, the produced JSON will be pretty-printed
                with the given number of indentation spaces
                (by default the produced JSON will be a compact
                one-line string)
    :type indent: Optional[int]

    :param sort_keys: Indicates whether to sort all maps in the produced
                JSON by the keys
    :type sort_keys: bool

    :return: The corresponding JSON string
    :rtype: string
    """
    return json.dumps(value, indent=indent, sort_keys=sort_keys)
