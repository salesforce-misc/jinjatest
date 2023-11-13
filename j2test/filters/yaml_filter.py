#!/usr/bin/env python3

import typing as t

from j2test.filters.yaml_utils import yaml_dumps_inline, yaml_loads


def to_yaml_filter(data: t.Any, indent: int = 0) -> str:
    return yaml_dumps_inline(data, indent=indent)


def from_yaml_filter(encoded: str) -> t.Dict[str, t.Any]:
    return yaml_loads(encoded)
