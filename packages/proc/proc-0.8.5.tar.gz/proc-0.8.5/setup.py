#!/usr/bin/env python

"""Setup script for the `proc` package."""

# Author: Peter Odding <peter@peterodding.com>
# Last Change: April 21, 2016
# URL: https://proc.readthedocs.org

# Standard library modules.
import codecs
import os
import sys

# De-facto standard solution for Python packaging.
from setuptools import find_packages, setup

# Find the directory where the source distribution was unpacked.
source_directory = os.path.dirname(os.path.abspath(__file__))

# Add the directory with the source distribution to the search path.
sys.path.append(source_directory)

# Import the module to find the version number (this is safe because the
# proc/__init__.py module doesn't import any external dependencies).
from proc import __version__ as version_string

# Fill in the long description (for the benefit of PyPI)
# with the contents of README.rst (rendered by GitHub).
readme_file = os.path.join(source_directory, 'README.rst')
with codecs.open(readme_file, 'r', 'utf-8') as handle:
    readme_text = handle.read()

setup(
    name='proc',
    version=version_string,
    description="Simple interface to Linux process information",
    long_description=readme_text,
    url='https://proc.readthedocs.org',
    author='Peter Odding',
    author_email='peter@peterodding.com',
    packages=find_packages(),
    entry_points=dict(console_scripts=[
        'cron-graceful = proc.cron:main',
        'notify-send-headless = proc.notify:main',
    ]),
    test_suite='proc.tests',
    install_requires=[
        'coloredlogs >= 5.0',
        'executor >= 9.9',
        'humanfriendly >= 1.35',
        'property-manager >= 1.2',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Operating System Kernels :: Linux',
        'Topic :: System :: Systems Administration',
        'Topic :: Terminals',
        'Topic :: Utilities',
    ])
