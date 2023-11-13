import j2test.utils as utils
import j2test.commons.j2test_messages as j2test_messages
import time
import sys
import os
import inspect
import typing
from termcolor import colored


class TestTemplate:
    """
        TestTemplate is the parent class of all jinja2 unit test classes.

        Child classes should extend the TestTemplate file and the run() method
        of the child class must be called (like in unittest).

        All functions within the child class that starts with "test" or "test_" and will automatically be run.
    """

    TEMPLATE_PATH = ""
    PRINT_ALL = True  # Need to find an elegant way of passing CLI flag to j2test class
    HEADER_WIDTH = 80

    _num_tests = 0
    _num_passed = 0
    _num_failed = 0
    _template = None
    _curr_failed = False
    _curr_method = ""
    _curr_path = ""
    _child_filename = ""

    def run(self) -> None:
        """
            Automatically runs all child class unit test functions that starts with "test" or "test_"
        """
        self._num_tests = 0
        self._num_passed = 0
        self._num_failed = 0

        start = time.time()

        # Get the path to file with the child test class
        child_path = os.path.abspath(inspect.getfile(self.__class__))
        self._curr_path = os.path.dirname(child_path)
        self._child_filename = os.path.basename(child_path)

        print(j2test_messages.START_MSG.format(
            filename=self._child_filename).center(self.HEADER_WIDTH, '='))

        # First set the Jinja Template
        self._set_template()

        # Get all the attributes of the child test class
        attrs = (getattr(self, name) for name in dir(self))

        # Iterate through the functions and only run the functions that starts with "test"
        for method in attrs:
            if callable(method) and method.__name__.startswith("test"):
                self._num_tests += 1
                self._curr_failed = False
                self._curr_method = method.__name__

                try:
                    # NOTE: Unit test functions should have no parameters like in unittest. Should either mock or
                    #       set varaibles instead. Thus, if an unit test has parameters will fail to in method call.
                    method()
                except TypeError as e:
                    self._curr_failed = True
                    print(j2test_messages.FAILED_TEST_CALL.format(
                        name=method.__name__, exception=e))

                if self._curr_failed:
                    self._num_failed += 1
                else:
                    self._num_passed += 1

        if self._num_tests == 0:
            print(colored(j2test_messages.NO_TESTS_FOUND.center(
                self.HEADER_WIDTH, '='), 'yellow'), end="\n\n")
            return

        end = time.time()
        total_time = round(end - start, 3)

        if self._num_tests == self._num_passed:
            print(colored(j2test_messages.PASS_MSG.
                          format(num_passed=self._num_passed, total_time=total_time).
                          center(self.HEADER_WIDTH, '='), 'green'), end="\n\n")
        else:
            print(colored(j2test_messages.FAIL_MSG.
                          format(num_failed=self._num_failed, num_tests=self._num_tests, total_time=total_time).
                          center(self.HEADER_WIDTH, '='), 'red'), end="\n\n")
            sys.exit(1)

    def assertEqualJsonFile(self, macro_name: str, args: any, expected_path: str) -> bool:
        """
            Asserts that the rendered JSON output and the expected JSON are the same.
            Renders the macro with the args passed in and retrieves the expected json file.
            It then compares the output and the expected output and ensures that the two JSON files are the same.

            :param macro_name: The name of macro function
            :type macro_name: str

            :param args: An array of arguments passed to the macro to render it
            :type args: [*]

            :param expected_path: Path relative to test file where expected JSON is
            :type expected_path: str

            :return: True if same and false otherwise
            :rtype: bool
        """
        if self._curr_failed is True:
            return False

        expected = self.loadJsonFile(expected_path)
        if expected is None:
            self._curr_failed = True
            return False

        return self.assertEqualJson(macro_name, args, expected)

    def assertNotEqualJsonFile(self, macro_name: str, args: any, expected_path: str) -> bool:
        """
            Asserts that the rendered JSON output and the expected JSON are different.
            Renders the macro with the args passed in and retrieves the expected json file.
            It then compares the output and the expected JSON and ensures that the 2 JSON files are NOT the same.

            :param macro_name: The name of macro function
            :type macro_name: str

            :param args: An array of arguments passed to the macro to render it
            :type args: [*]

            :param expected_path: Path relative to test file where expected JSON is
            :type expected_path: str

            :return: True if different and false if they are the same
            :rtype: bool
        """
        if self._curr_failed is True:
            return False

        expected = self.loadJsonFile(expected_path)
        if expected is None:
            self._curr_failed = True
            return False

        return self.assertNotEqualJson(macro_name, args, expected)

    def assertEqualJson(self, macro_name: str, args: any, expected: dict) -> bool:
        """
            Asserts that the rendered JSON output and the expected JSON are the same.
            Renders the macro with the args passed in and compares it with the expected output
            and ensures that the two JSON files are the same.

            :param macro_name: The name of macro function
            :type macro_name: str

            :param args: An array of arguments passed to the macro to render it
            :type args: [*]

            :param expected: dictionary
            :type expected: Dict[str, any]

            :return: True if same and false otherwise
            :rtype: bool
        """
        if self._curr_failed is True:
            return False

        output = self.render_macro_json(macro_name, args)
        result = utils.assert_json(output, expected)

        if result:
            return True
        elif output:
            print(colored(j2test_messages.FAILED_METHOD_NAME.
                          format(curr_method=self._curr_method).
                          center(self.HEADER_WIDTH, '_'), 'red'))
            print(j2test_messages.FAILED_ASSERT_EQ_JSON.format(macro_name=macro_name))
            utils.json_diff(output, expected, self.PRINT_ALL)
        else:
            print(colored(j2test_messages.FAILED_NO_JSON_OUTPUT.
                          format(curr_method=self._curr_method).
                          center(self.HEADER_WIDTH, '_'), 'red'))

        self._curr_failed = True
        return False

    def assertNotEqualJson(self, macro_name: str, args: any, expected: dict) -> bool:
        """
            Asserts that the rendered JSON output and the expected JSON are different.
            Renders the macro with the args passed in and compares it with the expected
            output and ensures that the two JSON files are NOT the same.

            :param macro_name: The name of macro function
            :type macro_name: str

            :param args: An array of arguments passed to the macro to render it
            :type args: [*]

            :param expected: dictionary
            :type expected: Dict[str, any]

            :return: True if different and false if they are the same
            :rtype: bool
        """
        if self._curr_failed is True:
            return False

        output = self.render_macro_json(macro_name, args)
        result = utils.assert_json(output, expected)

        if result:
            print(colored(j2test_messages.FAILED_METHOD_NAME.
                          format(curr_method=self._curr_method).
                          center(self.HEADER_WIDTH, '_'), 'red'))
            print(j2test_messages.FAILED_ASSERT_NEQ_JSON.format(
                macro_name=macro_name))
        elif output:
            return True
        else:
            print(colored(j2test_messages.FAILED_NO_JSON_OUTPUT.
                          format(curr_method=self._curr_method).
                          center(self.HEADER_WIDTH, '_'), 'red'))

        self._curr_failed = True
        return False

    def assertEqualString(self, macro_name: str, args: any, expected: str) -> bool:
        """
            Asserts that the rendered string output and the expected string are the same.
            Renders the macro with the args passed in and ensures the output is the same as the expected string.

            :param macro_name: The name of macro function
            :type macro_name: str

            :param args: An array of arguments passed to the macro to render it
            :type args: [*]

            :param expected: string
            :type expected: str

            :return: True if same and false otherwise
            :rtype: bool
        """
        if self._curr_failed is True:
            return False

        output = self.render_macro_str(macro_name, args)
        result = utils.assert_string(output, expected)

        if result:
            return True
        elif output:
            print(colored(j2test_messages.FAILED_METHOD_NAME.
                          format(curr_method=self._curr_method).
                          center(self.HEADER_WIDTH, '_'), 'red'))
            print(j2test_messages.FAILED_ASSERT_EQ_STR.format(
                macro_name=macro_name, expected=expected, output=output.strip()))
        else:
            print(colored(j2test_messages.FAILED_NO_STR_OUTPUT.
                          format(curr_method=self._curr_method).
                          center(self.HEADER_WIDTH, '_'), 'red'))

        self._curr_failed = True
        return False

    def assertNotEqualString(self, macro_name: str, args: any, expected: str) -> bool:
        """
            Asserts that the rendered string output and the expected string are different.
            Renders the macro with the args passed in and ensures the output is different from the expected string.

            :param macro_name: The name of macro function
            :type macro_name: str

            :param args: An array of arguments passed to the macro to render it
            :type args: [*]

            :param expected: Expected string value
            :type expected: str

            :return: True if different and false if the are the same
            :rtype: bool
        """
        if self._curr_failed is True:
            return False

        output = self.render_macro_str(macro_name, args)
        result = utils.assert_string(output, expected)

        if result:
            print(colored(j2test_messages.FAILED_METHOD_NAME.
                          format(curr_method=self._curr_method).
                          center(self.HEADER_WIDTH, '_'), 'red'))
            print(j2test_messages.FAILED_ASSERT_NEQ_STR.format(macro_name=macro_name))
        elif output:
            return True
        else:
            print(colored(j2test_messages.FAILED_NO_STR_OUTPUT.
                          format(curr_method=self._curr_method).
                          center(self.HEADER_WIDTH, '_'), 'red'))

        self._curr_failed = True
        return False

    def loadJsonFile(self, path: str) -> typing.Dict:
        """
            Gets the .json file and converts it to a python dictionary.

            :param path: Path relative to test file where json file is
            :type path: str

            :return: dictionary
            :rtype: Dict[str, any]
        """
        raw_path = os.path.join(self._curr_path, path)
        path = os.path.normpath(raw_path)
        dic = utils.get_json_file(path, self._curr_method)
        if dic is None:
            self._curr_failed = True
            return
        return dic

    def loadYamlFile(self, path: str) -> typing.Dict:
        """
            Gets the .yaml or .yml file and converts it to a python dictionary.

            :param path: Path relative to test file where YAML file is
            :type path: str

            :return: dictionary
            :rtype: Dict[str, any]
        """
        raw_path = os.path.join(self._curr_path, path)
        path = os.path.normpath(raw_path)
        dic = utils.get_yaml_file(path, self._curr_method)
        if dic is None:
            self._curr_failed = True
            return
        return dic

    def render_macro_json(self, macro_name: str, args: any) -> typing.Dict:
        """
            Gets JSON output of macro with checks to ensure macro and output is valid

            :param macro_name: Name of macro
            :type macro_name: str

            :param args: Array of arguments for the jinja macro
            :type args: [any*]

            :return: macro dictionary output
            :rtype: Dict[str, any]
        """
        macro = utils.get_macro(self.template, macro_name)
        if macro is None:
            self._curr_failed = True
            return

        output = utils.render_macro_json(macro, args)
        if output is None:
            self._curr_failed = True
            return
        return output

    def render_macro_str(self, macro_name: str, args: any) -> str:
        """
            Gets string output of macro with checks to ensure macro and output is valid

            :param macro_name: Name of macro
            :type macro_name: str

            :param args: Array of arguments for the jinja macro
            :type args: [any*]

            :return: macro string output
            :rtype: str
        """
        macro = utils.get_macro(self.template, macro_name)
        if macro is None:
            self._curr_failed = True
            return

        output = utils.render_macro_str(macro, args)
        if output is None:
            self._curr_failed = True
            return
        return output

    def _set_template(self) -> None:
        """
            Sets the jinja template for test and checks to ensure template is valid
            The path search order for the template file is: first explicit template path override,
            then the current directory of test file, and then the mirrored path relative to the
            closest jtests folder to the test file
        """
        env_path = self._curr_path

        if self.TEMPLATE_PATH == "":
            # Check in the current directory
            template_found = self._find_template_file(
                self._child_filename, env_path)

            # If nothing was found check if there is a jtests folder
            if template_found is False and "/jtests" in env_path:
                # Splits based on the last occurance
                res = env_path.rsplit('/jtests', 1)
                env_path = res[0]
                template_path = res[1]
                template_found = self._find_template_file(
                    self._child_filename, env_path, template_path)

        if self.TEMPLATE_PATH == "":
            print(j2test_messages.FAILED_NO_TEMPLATE.format(
                filename=self._child_filename, path=env_path))
            print(colored(j2test_messages.NO_TESTS_RUN.center(self.HEADER_WIDTH, '='), 'red'), end="\n\n")
            sys.exit(1)

        self.template = utils.get_template(self.TEMPLATE_PATH, env_path)

        if self.template is None:
            print(j2test_messages.FAILED_TO_GET_TEMPLATE.format(
                filename=self._child_filename, path=template_path))
            print(colored(j2test_messages.NO_TESTS_RUN.center(self.HEADER_WIDTH, '='), 'red'), end="\n\n")
            sys.exit(1)

    def _find_template_file(self, child_file_name: str, env_path: str, template_path: str = "") -> bool:
        """
            Finds the corresponding jinja template file

            :param child_file_name: jinja test file name
            :type child_file_name: str

            :param child_dir: Absolute path to jinja test file
            :type child_dir: str

            :return: True if jinja template file found, False otherwise
            :rtype: bool
        """
        if child_file_name.endswith('.py') and child_file_name.startswith('jtest_'):
            template_file = child_file_name[6:-3] + ".j2"
            template_path = os.path.join(template_path, template_file)
            if template_path and template_path.startswith('/'):
                template_path = template_path[1:]
            abs_path = os.path.join(env_path, template_path)
            if os.path.exists(abs_path):
                self.TEMPLATE_PATH = template_path
                return True
        return False
