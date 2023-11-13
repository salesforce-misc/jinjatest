"""
Helper filters for converting from native python types
to stringified hcl types (map, string)
"""

import rapidjson as json
import typing as t

# unique character string for later string substitution
ESCAPE_TOKEN = "!ESCAPE_TOKEN!"


def stringify_hcl_map_filter(data: t.Dict[str, str]) -> str:
    """
    Converts a python dictionary to a stringified HCL map
    e.g. {"key": "value"} ->
        "{key=\"value\"}"
    :param data: dictionary
    :type data: Dict[str, str]
    :return: string of stringified hcl map
    :rtype: str
    """
    hcl_list = ["{}=\"{}\"".format(k, v) for k, v in data.items()]
    result_raw = "{" + ",".join(hcl_list) + "}"
    stringified = json.dumps(result_raw)
    return stringified


def stringify_dict_filter(data: t.Dict[str, str]) -> str:
    """
    Used for packing a python dictionary into a
    Terraform compatible environment variable string
    compatible = no new lines, correct escaping of nested double-quotes

    This logic currently only handles two levels deep of double-quote escaping.

    e.g. {"level1: "{\"level2\":\"level2\"}"} ->
        "{\"level1\":\"{\\\"level2\\\":\\\"level2\\\"}\"}"

    :param data: python dictionary
    :type data: t.Dict[str, str]

    :return: Stingified dict, escapes double-quotes, removes whitespace chars
    :rtype: str
    """

    raw_string = str(data).replace("\"", ESCAPE_TOKEN)
    raw_json = json.dumps(raw_string)
    stringified = raw_json \
        .replace(ESCAPE_TOKEN, "\\\\\\\"")\
        .replace("'", "\\\"")\
        .replace("\n", "")\
        .replace(" ", "")
    return stringified
