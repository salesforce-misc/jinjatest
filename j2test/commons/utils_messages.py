TEMPLATE_NOT_FOUND = "ERROR: No template found in the path {template_path}\n"
TEMPLATE_SYNTAX_ERR = "ERROR: There is a template syntax error in {path}. No tests can be run until the following is resolved: \n{e}\n"
NO_MACRO_ERR = "ERROR: No macro named \"{macro}\" found in template.\n{e}\n"
PRIVATE_MACRO_ERR = "ERROR: You cannot test private jinja macros that starts with _ as they are inaccessible and cannot be imported. Please consider making the macro, \"{macro}\", public.\n"
INVALID_JSON_ERR = "ERROR: Failed to convert rendered macro output to JSON for the macro: {macro} for the following test:"
MACRO_ARGS_ERR = "ERROR: Arguments passed in does not match macro: {e}\n"
MACRO_RENDER_ERR = "ERROR: Failed to render macro: {macro}.\n{e}"
JSON_DECODER_ERR = "ERROR: JSON at {path} is invalid while running {method}.\n{e}\n"
JSON_LOAD_ERR = "ERROR: Failed to read in JSON file at: {path} while running {method}\n{e}\n"
INVALID_YAML_ERR = "ERROR: YAML at {path} is invalid while running {method}.\n{e}\n"
YAML_LOAD_ERR = "ERROR: Failed to read in YAML file at: {path} while running {method}\n{e}\n"
COMPARE_JSON_MSG = "\tExpected: {expected}\n\tBut got:  {output}\n"
DIFF_MSG = "Difference:\n{diff_map}\n"
INVALID_STR_TYPE = "\nERROR: Incorrect assert statement used. Expected strings for the macro output and expected value but got {expected_type} for expected and {output_type} for the macro output for the following test:"
INVALID_JSON_TYPE = "\nERROR: Incorrect assert statement used. Expected JSON for the macro output and expected value but got {expected_type} for expected and {output_type} for the macro output for the following test:"
