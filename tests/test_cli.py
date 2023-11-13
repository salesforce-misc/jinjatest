import pytest
from j2test import cli
import os

def test_run_valid():
    python_path = "./test_j2test.py"
    curr_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(curr_path, python_path)
    num_files = 0
    num_failed = 0
    num_files, num_failed = cli._run(path, num_files, num_failed)
    assert(num_files == 1)
    assert(num_failed == 0)

def test_run_invalid():
    path = "invalid.py"
    num_files = 0
    num_failed = 0
    num_files, num_failed = cli._run(path, num_files, num_failed)
    assert(num_files == 0)
    assert(num_failed == 1)