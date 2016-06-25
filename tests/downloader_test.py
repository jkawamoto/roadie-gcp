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
""" Test for downloader module.
"""
import logging
import shutil
import sys
import unittest
import os
from os import path
import downloader  # pylint: disable=import-error

TARGET_FILE = "bin/entrypoint.sh"

SAMPLE_FILE = "https://raw.githubusercontent.com/jkawamoto/roadie-gcp/master/bin/entrypoint.sh"
ORIGINAL_FILE = path.normpath(
    path.join(path.dirname(__file__), "..", TARGET_FILE))

ARCHIVE_ROOT = "./roadie-gcp-20160618"
ZIP_FILE = "https://github.com/jkawamoto/roadie-gcp/archive/v20160618.zip"
TAR_FILE = "https://github.com/jkawamoto/roadie-gcp/archive/v20160618.tar.gz"


class TestDownload(unittest.TestCase):
    """ Test case for download module.
    """

    def test_download(self):
        """ Test downloading a file.
        """
        downloader.download(SAMPLE_FILE)
        basename = path.basename(SAMPLE_FILE)
        self.evaluate_file(basename, ORIGINAL_FILE)
        os.remove(basename)

    def test_set_destination(self):
        """ Test downloading a file to another directory.
        """
        downloader.download(SAMPLE_FILE + ":/tmp/")
        target = "/tmp/" + path.basename(SAMPLE_FILE)
        self.evaluate_file(target, ORIGINAL_FILE)
        os.remove(target)

    def test_rename(self):
        """ Test downloading a file and renaming it.
        """
        target = "test.md"
        downloader.download(SAMPLE_FILE + ":" + target)
        self.evaluate_file(target, ORIGINAL_FILE)
        os.remove(target)

    def test_set_destination_and_rename(self):
        """ Test downloading a file to a directory and renaming it.
        """
        target = "/tmp/test.md"
        downloader.download(SAMPLE_FILE + ":" + target)
        self.evaluate_file(target, ORIGINAL_FILE)
        os.remove(target)

    def test_download_zip(self):
        """ Test downloading a zip file.
        """
        downloader.download(ZIP_FILE)
        target = path.join(ARCHIVE_ROOT, TARGET_FILE)
        self.evaluate_file(target, ORIGINAL_FILE)
        shutil.rmtree(ARCHIVE_ROOT)

    def test_set_destination_zip(self):
        """ Test downloading a zip file to a specified path.
        """
        downloader.download(ZIP_FILE + ":/tmp/")
        target = path.join("/tmp/", ARCHIVE_ROOT, TARGET_FILE)
        self.evaluate_file(target, ORIGINAL_FILE)
        shutil.rmtree(path.join("/tmp/", ARCHIVE_ROOT))

    def test_download_tarball(self):
        """ Test downloading a tarball file.
        """
        downloader.download(TAR_FILE)
        target = path.join(ARCHIVE_ROOT, TARGET_FILE)
        self.evaluate_file(target, ORIGINAL_FILE)
        shutil.rmtree(ARCHIVE_ROOT)

    def test_set_destination_taball(self):
        """ Test downloading a tarball file to a specified path.
        """
        downloader.download(TAR_FILE + ":/tmp/")
        target = path.join("/tmp/", ARCHIVE_ROOT, TARGET_FILE)
        self.evaluate_file(target, ORIGINAL_FILE)
        shutil.rmtree(path.join("/tmp/", ARCHIVE_ROOT))

    def evaluate_file(self, target, original):
        """ Evaluate existence and contents of the target file.

        Args:
          target: target file to be checked.
          original: original file of which contetns will be compared of the ones
                    of target.
        """
        self.assertTrue(path.exists(target))
        self.assertEqual(
            self.read_file(target),
            self.read_file(original))

    @staticmethod
    def read_file(fpath):
        """ Open a file and read it.

        Args:
          fpath: Path for a file.

        Returns:
          Contents of the file.
        """
        with open(fpath) as f:
            return f.read()




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    unittest.main()
