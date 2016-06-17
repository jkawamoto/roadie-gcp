#! /usr/bin/env python
""" Test for downloader module.
"""
import logging
import sys
import unittest
import os
from os import path
import downloader

SAMPLE_FILE = "https://raw.githubusercontent.com/jkawamoto/roadie-gcp/master/README.md"
ORIGINAL_FILE = path.normpath(path.join(path.dirname(__file__), "..", "README.md"))
print ORIGINAL_FILE


class TestDownloader(unittest.TestCase):
    """ Test case for download module.
    """
    def test_download(self):
        """ Test downloading a file.
        """
        downloader.download(SAMPLE_FILE)
        basename = path.basename(SAMPLE_FILE)
        self.assertTrue(path.exists(basename))
        self.assertEqual(
            TestDownloader.read_file(ORIGINAL_FILE),
            TestDownloader.read_file(basename))
        os.remove(basename)

    def test_set_destination(self):
        """ Test downloading a file to another directory.
        """
        downloader.download(SAMPLE_FILE + ":/tmp/")
        target = "/tmp/" + path.basename(SAMPLE_FILE)
        self.assertTrue(path.exists(target))
        self.assertEqual(
            TestDownloader.read_file(ORIGINAL_FILE),
            TestDownloader.read_file(target))
        os.remove(target)

    def test_rename(self):
        """ Test downloading a file and renaming it.
        """
        target = "test.md"
        downloader.download(SAMPLE_FILE + ":" + target)
        self.assertTrue(path.exists(target))
        self.assertEqual(
            TestDownloader.read_file(ORIGINAL_FILE),
            TestDownloader.read_file(target))
        os.remove(target)

    def test_set_destination_and_rename(self):
        """ Test downloading a file to a directory and renaming it.
        """
        target = "/tmp/test.md"
        downloader.download(SAMPLE_FILE + ":" + target)
        self.assertTrue(path.exists(target))
        self.assertEqual(
            TestDownloader.read_file(ORIGINAL_FILE),
            TestDownloader.read_file(target))
        os.remove(target)

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
