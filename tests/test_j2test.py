import pytest
import j2test


@pytest.fixture
def sample_test_template():
    # Mock jinja test object
    class AnotherTest(j2test.TestTemplate):
        TEMPLATE_PATH = "./templates/template.j2"

    template = AnotherTest()
    template.run()
    return template

def test_run(sample_test_template: j2test.TestTemplate):
    assert(sample_test_template._child_filename == "test_j2test.py")
    assert(sample_test_template.template != None)

def test_assert_equal_json_file(sample_test_template: j2test.TestTemplate):
    arr = ["value1", "value2"]
    macro = "template_macro"
    expected = sample_test_template.loadJsonFile("./expected/expected.json")

    result = sample_test_template.assertEqualJson(macro, arr, expected)
    assert(result == True)

def test_assert_not_equal_json_file(sample_test_template: j2test.TestTemplate):
    arr = ["invalid", "value2"]
    macro = "template_macro"
    expected = sample_test_template.loadJsonFile("./expected/expected.json")

    result = sample_test_template.assertNotEqualJson(macro, arr, expected)
    assert(result == True)

def test_assert_equal_json(sample_test_template: j2test.TestTemplate):
    arr = ["value1", "value2"]
    macro = "template_macro"
    expected = {"key1": "value1", "key2": "value2"}
    incorrect = {"key1": "what", "key2": "the"}

    result = sample_test_template.assertEqualJson(macro, arr, expected)
    assert(result == True)
    result = sample_test_template.assertEqualJson(macro, arr, incorrect)
    assert(result == False)


def test_assert_not_equal_json(sample_test_template: j2test.TestTemplate):
    arr = ["value1", "value2"]
    macro = "template_macro"
    not_expecting = {"key1": "value2", "key2": "value2"}
    expected = {"key1": "value1", "key2": "value2"}

    result = sample_test_template.assertNotEqualJson(macro, arr, not_expecting)
    assert(result == True)
    result = sample_test_template.assertNotEqualJson(macro, arr, expected)
    assert(result == False)

def test_assert_equal_str(sample_test_template: j2test.TestTemplate):
    data = "TEST"
    macro = "macro_str"
    arr = [data]

    result = sample_test_template.assertEqualString(macro, arr, data)
    assert(result == True)
    result = sample_test_template.assertEqualString(macro, arr, "INCORRECT")
    assert(result == False)


def test_assert_not_equal_str(sample_test_template: j2test.TestTemplate):
    data = "TEST"
    macro = "macro_str"
    arr = [data]

    result = sample_test_template.assertNotEqualString(macro, arr, "CORRECT")
    assert(result == True)
    result = sample_test_template.assertNotEqualString(macro, arr, data)
    assert(result == False)

def test_load_json_valid(sample_test_template: j2test.TestTemplate):
    expected = {"key1": "value1", "key2": "value2"}
    loaded_json = sample_test_template.loadJsonFile("./expected/expected.json")
    assert(expected == loaded_json)

def test_load_json_invalid(sample_test_template: j2test.TestTemplate):
    invalid = sample_test_template.loadJsonFile("./expected/invalid.json")
    assert(invalid == None)
    assert(sample_test_template._curr_failed == True)

def test_load_yaml_valid(sample_test_template: j2test.TestTemplate):
    loaded_yaml = sample_test_template.loadYamlFile("./variables/vars.yaml")
    assert(loaded_yaml != None)
    assert(loaded_yaml['std']['app']['team'] == "teamname")

def test_load_yaml_invalid(sample_test_template: j2test.TestTemplate):
    loaded_yaml = sample_test_template.loadYamlFile("./variables/invalid.yaml")
    assert(loaded_yaml == None)
    assert(sample_test_template._curr_failed == True)
