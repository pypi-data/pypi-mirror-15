#!/usr/bin/env python

"""Setup script for the `property-manager` package."""

# Author: Peter Odding <peter@peterodding.com>
# Last Change: June 1, 2016
# URL: https://property-manager.readthedocs.org

# Standard library modules.
import codecs
import os
import re

# De-facto standard solution for Python packaging.
from setuptools import setup, find_packages

# Find the directory where the source distribution was unpacked.
source_directory = os.path.dirname(os.path.abspath(__file__))

# Find the current version.
module = os.path.join(source_directory, 'property_manager', '__init__.py')
for line in open(module, 'r'):
    match = re.match(r'^__version__\s*=\s*["\']([^"\']+)["\']$', line)
    if match:
        version_string = match.group(1)
        break
else:
    raise Exception("Failed to extract version from %s!" % module)

# Fill in the long description (for the benefit of PyPI)
# with the contents of README.rst (rendered by GitHub).
readme_file = os.path.join(source_directory, 'README.rst')
with codecs.open(readme_file, 'r', 'utf-8') as handle:
    readme_text = handle.read()

setup(name="property-manager",
      version=version_string,
      description=("Useful property variants for Python programming (required"
                   " properties, writable properties, cached properties, etc)"),
      long_description=readme_text,
      url='https://property-manager.readthedocs.org',
      author="Peter Odding",
      author_email='peter@peterodding.com',
      packages=find_packages(),
      install_requires=[
          'humanfriendly >= 1.44.7',
          'verboselogs >= 1.1',
      ],
      tests_require=[
          'coloredlogs >= 5.0',
      ],
      test_suite='property_manager.tests',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Documentation :: Sphinx',
          'Topic :: Software Development',
          'Topic :: Software Development :: Documentation',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ])
