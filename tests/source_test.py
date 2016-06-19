#! /usr/bin/env python
#
# downloader_test.py
#
# Copyright (c) 2015-2016 Junpei Kawamoto
#
# This software is released under the MIT License.
#
# http://opensource.org/licenses/mit-license.php
#
""" Test for source method.
"""
import logging
import tempfile
import os
import os.path
import shutil
import sys
import unittest
from roadie import source  # pylint: disable=import-error


REPO_SSH = "git@github.com:jkawamoto/roadie-gcp.git"
REPO_HTTPS = "https://github.com/jkawamoto/roadie-gcp.git"
CHECK_FILE = "README.md"

_SSH_TEST = "SSH_TEST"


class TestSource(unittest.TestCase):
    """ Test case for source method.

    Skip testing of `url` sectiong because it is depened on download module and
    we have other tests for the module.
    """

    def setUp(self):
        """ Create a temporal directory.
        """
        self.dir = tempfile.mkdtemp(dir=".")

    def tearDown(self):
        """ Remove the temporal directory setUp made.
        """
        shutil.rmtree(self.dir)

    @unittest.skipUnless(
        _SSH_TEST in os.environ and bool(os.environ[_SSH_TEST]),
        "This test requires to deploy ssh key.")
    def test_clone_via_ssh(self):
        """ Test downloading a file.
        """
        source(REPO_SSH, self.dir)
        with open(os.path.join(self.dir, CHECK_FILE)) as res:
            with open(CHECK_FILE) as ans:
                self.assertEqual(res.read(), ans.read())

    def test_clone_via_https(self):
        """ Test downloading a file.
        """
        source(REPO_HTTPS, self.dir)
        with open(os.path.join(self.dir, CHECK_FILE)) as res:
            with open(CHECK_FILE) as ans:
                self.assertEqual(res.read(), ans.read())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    unittest.main()
