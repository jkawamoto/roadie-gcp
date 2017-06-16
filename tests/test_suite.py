#! /usr/bin/env python
#
# test_suite.py
#
# Copyright (c) 2015-2017 Junpei Kawamoto
#
# This software is released under the MIT License.
#
# http://opensource.org/licenses/mit-license.php
#
""" Test suite.
"""
from __future__ import absolute_import
import sys
import unittest

import tests.downloader_test
import tests.source_test


def suite():
    """ Return a test suite.
    """
    loader = unittest.TestLoader()
    res = unittest.TestSuite()
    res.addTest(loader.loadTestsFromModule(tests.downloader_test))
    res.addTest(loader.loadTestsFromModule(tests.source_test))
    return res


def main():
    """ The main function.

    Returns:
      exit code.
    """
    try:
        res = unittest.TextTestRunner(verbosity=2).run(suite())
    except KeyboardInterrupt:
        return -1
    else:
        return 0 if res.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
