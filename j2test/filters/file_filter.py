#!/usr/bin/env python3

from jinja2.utils import pass_context
import os
import typing as t

from j2test.filters.yaml_utils import yaml_dump


def write_to_file_filter(data: t.Any, file_path: str) -> t.Any:
    with open(file_path, "w") as f:
        if isinstance(data, str):
            f.write(data + "\n")
        else:
            yaml_dump(data, f)

    return data


@pass_context
def read_from_file(context: t.Any, file_path: str) -> str:
    real_path = context.environment.loader.searchpath[0] + os.path.sep + file_path
    with open(real_path) as f:
        return str(f.read())
