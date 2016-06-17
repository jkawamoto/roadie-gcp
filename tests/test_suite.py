#! /usr/bin/env python
""" Test suite.
"""
from __future__ import absolute_import
import sys
import unittest

from . import downloader_test

def suite():
    """ Return a test suite.
    """
    loader = unittest.TestLoader()
    res = unittest.TestSuite()
    res.addTest(loader.loadTestsFromModule(downloader_test))
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
