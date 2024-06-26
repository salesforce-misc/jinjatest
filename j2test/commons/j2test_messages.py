START_MSG = " Jinja2 test session starts for {filename} "
PASS_MSG = " {num_passed} passed in {total_time} seconds "
FAIL_MSG = " {num_failed} failed out of {num_tests} in {total_time} seconds "
FAILED_METHOD_NAME = " {curr_method} "
FAILED_NO_JSON_OUTPUT = " {curr_method} failed due to no JSON output "
FAILED_NO_STR_OUTPUT = " {curr_method} failed due to no str output "
NO_TESTS_FOUND = " no tests found "
NO_TESTS_RUN = " no tests were run "

FAILED_TEST_CALL = "Failed to call {name}. {excpetion}\n"
FAILED_ASSERT_EQ_JSON = "Macro: {macro_name}\nassertEqualJson failed.\n"
FAILED_ASSERT_NEQ_JSON = "Macro: {macro_name}\nassertNotEqualJson failed. Expected output and expected to be different but are the same.\n"
FAILED_ASSERT_EQ_STR = "Macro: {macro_name}\nassertEqualString failed.\n\tExpected: {expected}\n\tBut got:  {output}\n"
FAILED_ASSERT_NEQ_STR = "Macro: {macro_name}\nassertNotEqualString failed. Expected output and expected to be different but are the same.\n"
FAILED_NO_TEMPLATE = "ERROR: No template file provided or no corresponding template could be found for {filename}. Ensure it ends with .j2 and follows a valid directory structure. Checked in {path}\n"
FAILED_TO_GET_TEMPLATE = "ERROR: Failed to get template for {filename} in {path}\n"
