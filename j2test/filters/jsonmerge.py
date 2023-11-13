#!/usr/bin/env python3

import jsonmerge
import typing as t


def jsonmerge_filter(
    base: t.Any,
    override: t.Any,
) -> t.Any:
    """
    Merges one object on top of the other following the typical
    merging rules for JSON objects.

    For example, dictionaries are merged logically: the same keys
    are replaced, new keys are added, existing keys are kept as is.
    Values of all other types are replaced as a whole.

    The merging is performed recursively.

    :param base: The object to merge changes into
    :type base: Any

    :param override: The object to merge changes from
    :type override: Any

    :return: The merged object
    :rtype: Any
    """

    return jsonmerge.merge(base, override)
