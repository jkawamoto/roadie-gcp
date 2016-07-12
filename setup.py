#
# setup.py
#
# Copyright (c) 2015-2016 Junpei Kawamoto
#
# This software is released under the MIT License.
#
# http://opensource.org/licenses/mit-license.php
#
""" roadie-gcp package information.
"""
from setuptools import setup, find_packages
import sys

sys.path.append("bin")


setup(
    name='roadie-gcp',
    version='0.9.0',
    description="A helper to execute a program on Google Cloud Platform.",
    author="Junpei Kawamoto",
    author_email="kawamoto.junpei@gmail.com",
    url="https://github.com/jkawamoto/roadie-gcp",
    packages=find_packages(exclude=["tests"]),
    test_suite='tests.suite',
    license="MIT"
)
