#!/usr/bin/env python3
import re


def regex_replace(expression: str, replacement: str, input_str: str) -> str:

    """
    Regex Search and Replace functionality implemented for Jinja templates
    """
    return re.sub(expression, replacement, input_str)
