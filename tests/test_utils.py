import pytest
import jinja2
import os
from j2test import utils

@pytest.fixture
def sample_template():
    template_path = "./templates/context.j2"
    curr_path = os.path.dirname(os.path.abspath(__file__))
    return utils.get_template(template_path, curr_path)

def test_get_template(sample_template: jinja2.Template):
    assert(sample_template != None)

def test_get_macro_valid(sample_template: jinja2.Template):
    macro_name = "get_request_level"
    macro = utils.get_macro(sample_template, macro_name)
    assert(macro != None)

def test_get_macro_invalid(sample_template: jinja2.Template):
    macro_name = "does_not_exist"
    macro = utils.get_macro(sample_template, macro_name)
    assert(macro == None)

def test_get_macro_private(sample_template: jinja2.Template):
    macro_name = "_some_private_macro"
    macro = utils.get_macro(sample_template, macro_name)
    assert(macro == None)

def test_macro_json(sample_template: jinja2.Template):
    macro_name = "get_request_meta"
    data = {"std": {"env": {"instance": "NONE", "server": "NONE", "datacenter": {"region": "region1", "type": "some_type"}}}}
    args = [data, "test"]
    expected = {'case_types': 'test', 'datacenter_type': 'some_type', 'region_name': 'region1', 'level': 'DATACENTER'}

    macro = utils.get_macro(sample_template, macro_name)
    rendered_json = utils.render_macro_json(macro, args)
    assert(rendered_json == expected)
    assert(utils.assert_json(rendered_json, expected) == True)

def test_macro_str(sample_template: jinja2.Template):
    macro_name = "get_request_level"
    data = {"std": {"env": {"instance": "NONE", "server": "server123", "datacenter": {"region": "region1", "type": "some_type"}}}}
    args = [data]

    macro = utils.get_macro(sample_template, macro_name)
    rendered_str = utils.render_macro_str(macro, args)
    assert(utils.assert_string(rendered_str, "SERVER") == True)

def test_assert_json():
    dic1 = {"key1": "value1", "key2": "value2"}
    dic2 = {"key2": "value2", "key1": "value1"}
    diff3 = {"key1": "different", "key2": "value2"}
    assert(utils.assert_json(dic1, dic2) == True)
    assert(utils.assert_json(dic1, diff3) == False)

def test_get_json_file():
    json_path = "./values/vals.json"
    curr_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(curr_path, json_path)
    json = utils.get_json_file(path, "test_utils")
    assert(json != None)
    assert(json[0]["target"]["name"] == "mock_target_name.json")

def test_assert_string():
    str1 = "TEST"
    str2 = "        TEST\n     "
    str_diff = "DIFF_TEST"

    assert(utils.assert_string(str1, str2) == True)
    assert(utils.assert_string(str1, str_diff) == False)

def test_json_diff():
    dic1 = {"key1": "value1", "key2": "value2"}
    dic2 = {"key2": "value2", "key1": "value1"}
    diff3 = {"key1": "different", "key2": "value2"}
    expected_diff = {'values_changed': {"root['key1']": {'new_value': 'value1', 'old_value': 'different'}}}

    assert(utils.json_diff(dic1, dic2) == {})
    assert(utils.json_diff(dic1, diff3) == expected_diff)
