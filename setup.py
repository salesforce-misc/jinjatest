from setuptools import find_packages, setup
import re

VERSIONFILE="j2test/_version.py"
version_line = open(VERSIONFILE, "rt").read()
version_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
matches = re.search(version_regex, version_line, re.M)
if matches:
    version_number = matches.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(
    name='j2test',
    packages=find_packages(exclude=["tests"]),
    version=version_number,
    description='Jinja2 Macro Unit Testing Library',
    author='Zemann Sheen',
    license='Apache License',
    install_requires=[
        'jinja2==3.0.3',
        'termcolor',
        'deepdiff',
        'pyyaml',
        'jsonmerge',
        'jsonpath',
        'ruamel.yaml',
        'python-rapidjson'
    ],
    entry_points={
        'console_scripts': [
            'j2test = j2test.cli:main'
        ]
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
