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
import sys
from setuptools import setup, find_packages
sys.path.append("bin")

setup(
    name="roadie-gcp",
    use_scm_version=True,
    description="A helper to execute a program on Google Cloud Platform.",
    author="Junpei Kawamoto",
    author_email="kawamoto.junpei@gmail.com",
    url="https://github.com/jkawamoto/roadie-gcp",
    packages=find_packages(exclude=["tests"]),
    setup_requires=[
        "setuptools_scm"
    ],
    test_suite="tests.suite",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries",
    ]
)
