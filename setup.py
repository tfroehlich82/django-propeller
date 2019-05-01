#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import django2_propeller

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = django2_propeller.__version__

if sys.argv[-1] == 'publish':
    os.system('cd docs && make html')
    os.system('python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*')
    sys.exit()

if sys.argv[-1] == 'test':
    print("Running tests only on current environment.")
    print("Use `tox` for testing multiple environments.")
    os.system('python manage.py test')
    sys.exit()

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='django2-propeller',
    version=version,
    description="""Propeller support for Django projects""",
    long_description=readme + '\n',
    author='Adam Radestock',
    author_email='raddishiow@gmail.com   ',
    url='https://github.com/RaddishIoW/django2-propeller',
    packages=[
        'django2_propeller',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=2.0,<3.0'
    ],
    license="MIT License",
    zip_safe=False,
    keywords='django2-propeller',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
    ],
)
