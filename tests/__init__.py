#
# __init__.py
#
# Copyright (c) 2015-2017 Junpei Kawamoto
#
# This software is released under the MIT License.
#
# http://opensource.org/licenses/mit-license.php
#
"""Unit test for roadie-gcp.
"""
from __future__ import absolute_import
import logging
import sys
sys.path.append("bin")
from tests.test_suite import suite

logging.basicConfig(level=logging.INFO)
