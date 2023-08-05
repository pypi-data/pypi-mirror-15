# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import os
import re

from setuptools.command.test import test as TestCommand
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


class PyTest(TestCommand):
    '''Pytest command.'''

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        '''Import pytest and run.'''
        import pytest
        errno = pytest.main(self.test_args)
        raise SystemExit(errno)


with open(os.path.join(
    os.path.dirname(__file__), 'source', 'clique', '_version.py'
)) as _version_file:
    _version = re.match(
        r'.*__version__ = \'(.*?)\'', _version_file.read(), re.DOTALL
    ).group(1)


setup(
    name='Clique',
    version=_version,
    description='Manage collections with common numerical component.',
    long_description=open('README.rst').read(),
    keywords='sequence, pattern, filesystem, collection, numerical',
    url='https://github.com/4degrees/clique',
    author='Martin Pengelly-Phillips',
    author_email='martin@4degrees.ltd.uk',
    license='Apache License (2.0)',
    packages=[
        'clique',
    ],
    package_dir={
        '': 'source'
    },
    install_requires=[
    ],
    tests_require=['pytest >= 2.3.5'],
    cmdclass={
        'test': PyTest
    },
    zip_safe=False
)

