#!/usr/bin/python3
import os
import sys
from setuptools.command.test import test as TestCommandBase

PACKAGE_NAME = "knittingpattern"
PACKAGE_NAMES = [
        "knittingpattern",
        "knittingpattern.convert", "knittingpattern.convert.test"
    ]

__doc__ = '''
The setup and build script for the {} library.
'''.format(PACKAGE_NAME)
__version__ = __import__(PACKAGE_NAME).__version__
__author__ = 'Nicco Kunzmann'

HERE = os.path.dirname(__file__)


def read_file_named(file_name):
    file_path = os.path.join(HERE, file_name)
    with open(file_path) as f:
        return f.read()


def read_filled_lines_from_file_named(file_name):
    content = read_file_named("requirements-test.txt")
    lines = content.splitlines()
    return [line for line in lines if line]


# The base package metadata to be used by both distutils and setuptools
METADATA = dict(
    name=PACKAGE_NAME,
    version=__version__,
    packages=PACKAGE_NAMES,
    author=__author__,
    author_email='niccokunzmann@rambler.ru',
    description='Python library for knitting machines.',
    license='LGPL',
    url='https://github.com/AllYarnsAreBeautiful/' + PACKAGE_NAME,
    keywords='knitting ayab fashion',
)

# Run tests in setup


class TestCommand(TestCommandBase):

    TEST_ARGS = [PACKAGE_NAME]

    def finalize_options(self):
        TestCommandBase.finalize_options(self)
        self.test_suite = True
        self.test_args = self.TEST_ARGS

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


class CoverageTestCommand(TestCommand):
    TEST_ARGS = [PACKAGE_NAME, "--cov=" + PACKAGE_NAME]


class PEP8TestCommand(TestCommand):
    TEST_ARGS = [PACKAGE_NAME, "--pep8"]


class FlakesTestCommand(TestCommand):
    TEST_ARGS = [PACKAGE_NAME, "--flakes"]


class CoveragePEP8TestCommand(TestCommand):
    TEST_ARGS = [PACKAGE_NAME, "--cov=" + PACKAGE_NAME, "--pep8"]


class LintCommand(TestCommandBase):

    def finalize_options(self):
        TestCommandBase.finalize_options(self)
        self.test_suite = True
        self.test_args = [PACKAGE_NAME]

    def run_tests(self):
        from pylint.lint import Run
        Run(self.test_args)

# Extra package metadata to be used only if setuptools is installed
required_packages = \
    read_filled_lines_from_file_named("requirements.txt")
required_test_packages = \
    read_filled_lines_from_file_named("requirements-test.txt")

DEVELOPMENT_STATES = {
        "p": "Development Status :: 1 - Planning",
        "pa": "Development Status :: 2 - Pre-Alpha",
        "a": "Development Status :: 3 - Alpha",
        "b": "Development Status :: 4 - Beta",
        "": "Development Status :: 5 - Production/Stable",
        "m": "Development Status :: 6 - Mature",
        "i": "Development Status :: 7 - Inactive"
    }
development_state = DEVELOPMENT_STATES[""]
for ending in DEVELOPMENT_STATES:
    if ending and __version__.endswith(ending):
        development_state = DEVELOPMENT_STATES[ending]

SETUPTOOLS_METADATA = dict(
    install_requires=required_packages,
    tests_require=required_test_packages,
    include_package_data=True,
    classifiers=[  # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License'
        ' v3 (LGPLv3)',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Artistic Software',
        'Topic :: Home Automation',
        'Topic :: Utilities',
        'Intended Audience :: Manufacturing',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        development_state
        ],
    package_data=dict(
        # If any package contains of these files, include them:
        knitting=['*.json'],
    ),
    zip_safe=False,
    cmdclass={
        "test": TestCommand,
        "coverage": CoverageTestCommand,
        "coverage_test": CoverageTestCommand,
        "pep8": PEP8TestCommand,
        "pep8_test": PEP8TestCommand,
        "flakes": FlakesTestCommand,
        "fakes_test": FlakesTestCommand,
        "coverage_pep8_test": CoveragePEP8TestCommand,
        "lint": LintCommand,
        },
)


def main():
    # Build the long_description from the README and CHANGES
    METADATA['long_description'] = read_file_named("README.rst")

    # Use setuptools if available, otherwise fallback and use distutils
    try:
        import setuptools
        METADATA.update(SETUPTOOLS_METADATA)
        setuptools.setup(**METADATA)
    except ImportError:
        import distutils.core
        distutils.core.setup(**METADATA)

if __name__ == '__main__':
    main()
