#!/usr/bin/env python3

import io
import ruamel.yaml
import typing as t


def yaml_load(yml_fp: t.Union[t.TextIO, t.BinaryIO]) -> t.Dict[str, t.Any]:
    # yaml.load is polymorphic, but we'll hide that here for mypy
    return yaml_loads(yml_fp)  # type: ignore


def yaml_dump(data: t.Dict[str, t.Any], fp: t.TextIO) -> None:
    yaml = ruamel.yaml.YAML(typ="rt")
    yaml.dump(data, stream=fp)


def yaml_loads(yml_data: str) -> t.Dict[str, t.Any]:
    yaml = ruamel.yaml.YAML(typ="safe")
    return yaml.load(yml_data)


def yaml_dumps(data: t.Dict[str, t.Any]) -> str:
    string_stream = io.StringIO()
    yaml_dump(data, string_stream)
    return string_stream.getvalue()


def yaml_dumps_inline(data: t.Dict[str, t.Any], indent: int) -> str:
    """
    indent - How many spaces to indent each line, except the first
    inline - If False, treat data as an entire document
    """
    val = yaml_dumps(data)

    # Below this line, we're just encoding a fragment.

    lines = val.split("\n")
    new_lines = [lines[0]]  # don't indent the first line
    for line in lines[1:]:
        if line == "...":
            # inline means "not a document", so don't allow an end token
            continue
        new_lines.append("{}{}".format("".rjust(indent), line))

    # ruamel.yaml always adds an extra newline; kill it
    if new_lines[-1].strip() == "":
        new_lines = new_lines[:-1]

    return "\n".join(new_lines)
