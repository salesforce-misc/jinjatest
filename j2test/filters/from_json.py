import rapidjson as json
import typing as t


def from_json_filter(data: str) -> t.Any:
    """
    A wrapper around json.loads(), which unmarshals a string representation
    of a JSON object into its equivalent JSON object

    :param data: The string representation of the JSON object
    :type data: str

    :return: The corresponding JSON object
    :rtype: Any
    """
    return json.loads(data)
