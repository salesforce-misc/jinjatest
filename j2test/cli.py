import argparse
import os
import sys
import typing
import j2test.commons.cli_messages as cli_messages
from j2test._version import __version__


def main() -> None:
    """
        Main entrance for the j2test CLI component.
    """
    num_files = 0
    num_failed = 0

    parser = argparse.ArgumentParser(prog='j2test',
                                    usage='%(prog)s [options] file',
                                    description='Jinja2 Macro Unit Testing Framework')

    parser.add_argument('file', metavar='file', type=str, default='all', nargs='?',
                        help=("(Optional) Python unit test file name or do not pass in a file name to "
                            "recursively call all j2test files under the current directory."))

    parser.add_argument('-v', '--version', action='version', version='%(prog)s {version}'.format(version=__version__))

    args = parser.parse_args()
    test_file_path = args.file

    if test_file_path == 'all':
        # Case where we recursively find all jinja test files under the current directory and run them
        for root, _, files in os.walk('./'):
            for file in files:
                if(file.endswith(".py") and file.startswith("jtest_")):
                    raw_script_path = os.path.join(root, file)
                    script_path = os.path.normpath(raw_script_path)
                    num_files, num_failed = _run(script_path, num_files, num_failed)
    elif test_file_path and os.path.isfile(test_file_path):
        # Case where a single jinja test file is passed in
        if test_file_path.endswith('.py'):
            num_files, num_failed = _run(test_file_path, num_files, num_failed)
        else:
            print(cli_messages.INVALID_TEST_FILE)
    else:
        # Case where file path passed in does not exist
        print(cli_messages.NO_TEST_FILE.format(file=test_file_path))
        sys.exit(1)

    print(cli_messages.FINAL_MSG.format(num_files=num_files))

    if num_failed != 0:
        sys.exit(1)


def _run(path: str, num_files: int, num_failed: int) -> typing.Tuple:
    """
        Calls the jinja2 test file to be run and increments the number of total files run if successful.

        :param path: The path to the unit test file
        :type path: str

        :param num_files: Number of jinja unit test files run so far
        :type num_files: int

        :param num_failed: Number of jinja unit test files failed
        :type num_failed: int

        :return: number of unit test files run, number of unit test files failed
        :rtype: Tuple[int, int]
    """
    try:
        # Note: Should find a more elegant way of calling test files while not changing the context
        if os.path.exists(path):
            return_code = os.system("python3 " + path)
            num_files += 1
            if return_code != 0:
                num_failed += 1
        else:
            print(cli_messages.NO_TEST_FILE_FOUND.format(path=path))
            num_failed += 1
        return num_files, num_failed
    except Exception as e:
        print(cli_messages.RUN_FAILED.format(path=path, e=e))
