#!/usr/bin/env python
__license__ = """
Copyright 2015 Parse.ly, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import re
import sys

from setuptools import setup, find_packages

# Get version without importing, which avoids dependency issues


def get_version():
    with open('jxwechattool/__init__.py') as version_file:
        return re.search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
                         version_file.read()).group('version')

install_requires = [
    'redis',
    'requests',
]

# tests_require = ['mock', 'nose', 'unittest2', 'python-snappy']
dependency_links = []

setup(
    name='jxwechattool',
    version=get_version(),
    author='jianxun_dev',
    author_email='dev@huntcoder.com',
    url='https://jianxun.io',
    description='pywechat access_token qrcode',
    keywords='pywechat access_token qrcode',
    license='Apache License 2.0',
    packages=find_packages(),
    install_requires=install_requires,
    dependency_links=dependency_links,
    zip_safe=False,
    include_package_data=True,
)
