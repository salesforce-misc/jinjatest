# J2Test: Jinja2 Unit Test Framework

## Table of Contents
- Background
- Installation
- Usage
- Contribute
- License

## Background
The `J2Test` framework makes it easy to write unit tests for Jinja2 macros in a simple and scalable manner. It provides powerful features such as macro rendering, macro output assertions, custom Jinja filters, and a CLI tool for test automation.

`J2Test` was developed to be able to build robust unit tests for Jinja macros by eliminating the overhead of importing, running, and testing Jinja macros.


## Installation

1a. Run the following command in your command line:
```bash
pip3 install sfdc-j2test
```

1b. Alternatively, install via Github
```bash
git clone git@github.com:salesforce-misc/jinjatest.git
cd jinjatest
pip install -e .
```

2. Verify it works:
```bash
j2test --version
```


## Usage
### Creating your first test
1. Create a python test file and name it  `jtest_<JINJA_FILENAME>.py`.
2. Within the test file, `import j2test` and create a class that extends the `j2test.TestTemplate` object from the j2test package.
3. That's it. Now write your unit tests! J2Test will automatically run all the functions that start with `test` or `test_`.

```
import j2test

class SomeTest(j2test.TestTemplate):
    macro = "template_macro"

    def test_something1(self):
        arr = [...]
        self.assertEqualJsonFile(self.macro, arr, "./expected.json")

    def test_something2(self):
        arr = [...]
        expected = { ... }
        self.assertEqualJson(self.macro, arr, expected)

    def testSomething3(self):
        arr = [...]
        expected = "VALUE"
        self.assertEqualString(self.macro, arr, expected)

    def invalid_test(self):
        # Note: This will not run as it does not start with "test" or "test_"

if __name__ == '__main__':
    SomeTest().run()
```

### Running your unit tests
- To run a single j2test file:
```bash
j2test jtest_<JINJA_FILENAME>.py
```
- To run all j2test files under the current directory (this will automatically and recursively find and run all jinja test files, similar to pytest):
```bash
j2test
```

### Conventions
- All test files must follow `jtest_<JINJA_FILENAME>.py`
- All unit test functions must start with `test` or `test_`
- All unit test function names must be unique
- The jinja test folder(s) must be named `jtests`. Check out the j2test [Test Directory Structure](#test-directory-structure) section below.
- The jinja import base directory is set to the parent directory in which the `j2tests` folder is in or if there is no `j2tests` folder, it is wherever the j2test file is located. This is important if you have imports within your jinja file.
- File paths specified in the test file, such as JSON/YAML files, must be specified relative to the test file. j2test will automatically convert relative file paths for you!
- This framework uses a class structure instead of functions at the file level. (for ease of use as users will be using far more functions from the package than in the Python unit testing framework [pytest](https://github.com/pytest-dev/pytest/) and also introduces more structure.
- Beware of jinja requirements as well. For example, private macros, macros that start with `_`, cannot be tested as it's not accessible. So make macros public if you wish to test them.


## Test Directory Structure
j2test supports 3 common test directory structures. Like in pytest, j2test will automatically match the j2test test file with the jinja file using the name of the test file.

1. Test file and Jinja template at the same level
```
app.j2
jtest_app.py
```
2. Tests folder at the application level (Recommended)
```
src/
    __init__.py
    appmodule.j2
    module1/
        part1.j2
        part2.j2
    ...
jtests/
    src/
        jtest_appmodule.py
        module1/
            jtest_part1.py
            jtest_part2.py
        ...
```
3. Inlining test directories into your application package
```
src/
    __init__.py
    appmodule.j2
    jtests/
        jtest_appmodule.py
    module1/
        part1.j2
        part2.j2
        jtests/
            jtest_part1.py
            jtest_part2.py
    ...
```

### J2Test Functions
|Function |Args & Return type |Description|
|:------|:------|:------|
|`assertEqualJsonFile`| `macro_name`: str, `args`: [any], `expected_path`: str &#8594; bool| Asserts that the rendered JSON output from the macro and the expected JSON file are the same.|
|`assertEqualJson`| `macro_name`: str, `args`: [any], `expected`: dict &#8594; bool| Asserts that the rendered JSON output from the macro and the expected JSON are the same.|
|`assertEqualString`| `macro_name`: str, `args`: [any], `expected`: str &#8594; bool| Asserts that the rendered string output from the macro and the expected string are the same.|
|`render_macro_json`| `macro_name`: str, `args`: [any] &#8594; dict| Gets the JSON output of the macro. |
|`render_macro_str`| `macro_name`: str, `args`: [any] &#8594; str| Gets the string output of macro, no formatting is done on the macro output. |
|`loadJsonFile`| `path`: str &#8594; dict| Gets the .json file and converts it to a Python dictionary.|
|`loadYamlFile`| `path`: str &#8594; dict| Gets the .yaml or .yml file and converts it to a Python dictionary.|

Note: All assertion functions have the corresponding negation functions such as `assertNotEqualJsonFile`, `assertNotEqualJson`, and `assertNotEqualString`.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Contribution [details](https://github.com/salesforce-misc/jinjatest/blob/main/CONTRIBUTING.md) can be found here. Please make sure to update tests as appropriate.

## License
By contributing your code, you agree to license your contribution under the terms of our project [LICENSE](LICENSE.txt) and to sign the [Salesforce CLA](https://cla.salesforce.com/sign-cla)
