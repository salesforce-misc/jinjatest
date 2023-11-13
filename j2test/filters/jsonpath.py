#!/usr/bin/env python3

import jsonpath
import typing as t


def jsonpath_filter(
    value: t.Any,
    jpath: str,
) -> t.Optional[t.List[t.Any]]:
    """
    A wrapper around jsonpath.jsonpath(), which exposes no arguments.

    :param value: The object to parse with jsonpath
    :type value: Any

    :param jpath: A JSON path string
    :type jpath: str

    :return: Sub-object at JSON path, or None
    :rtype: Optional[List[Any]]
    """
    p = jsonpath.jsonpath(value, jpath)

    # NOTE: jsonpath() wraps the return value in a list except for error cases.
    #       If there is an error, it simply returns False without a list.
    if p is False:
        return None

    assert isinstance(p, list)
    return p
