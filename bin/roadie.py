#! /usr/bin/env python
#
# roadie.py
#
# Copyright (c) 2015 Junpei Kawamoto
#
# This software is released under the MIT License.
#
# http://opensource.org/licenses/mit-license.php
#
""" The main module of roadie-gcp.
"""
import argparse
import glob
import logging
import os
import subprocess
import sys
import yaml
from downloader import download
import shutdown

# Template path of temporary files.
TEMPPATH = "/tmp/stdout{0}.txt"

# Static variables.
SOURCE = "source"
DATA = "data"
RUN = "run"
RESULT = "result"
DESTINATION = "destination"
PATTERN = "pattern"

GIT = "git"
URL = "url"

LOGGER = logging.getLogger(__name__)


def source(conf, cwd=None):
    """ Prepare source files from git, dropbox, gs, and/or web.

    Args:
      conf: a part of configure object.
      cwd: working directory. (Default: current directory)
    """
    if not cwd:
        cwd = "."

    if GIT in conf:
        path = conf[GIT]
        proc = subprocess.Popen(
            ["git", "clone", path, "."], stdout=sys.stdout, cwd=cwd)
        proc.communicate()

    if URL in conf:
        path = conf[URL]
        download(path)

    pkg = os.path.join(cwd, "requirements.in")
    if os.path.exists(pkg):
        proc = subprocess.Popen(
            ["pip-compile", pkg], stdout=sys.stdout)
        proc.communicate()

    pkg = os.path.join(cwd, "requirements.txt")
    if os.path.exists(pkg):
        proc = subprocess.Popen(
            ["pip", "install", "-r", pkg], stdout=sys.stdout)
        proc.communicate()


def execute(command, stdout, stderr=sys.stdout):
    """ Run a given command.

    Args:
      command: a string specifying command to be run.
      stdout: Writable object to which stdout of subprocess connects.
      stderr: Writable object to which stderr of subprocess connects.
    """
    # Does tail work to watch stdout to logging service?
    proc = subprocess.Popen(
        command, shell=True, stdout=stdout, stderr=stderr)
    proc.wait()


def upload(pat, dest):
    """ Upload objects matched to a given pattern.

    Args:
      pat: Pattern of objects to be uploaded.
      dest: Destination URL.
    """
    proc = subprocess.Popen(
        ["gsutil", "cp", pat, dest], stdout=sys.stdout)
    proc.wait()


# whether runner should stop when getting status codes not 0?
def run(conf, halt, unzip):
    """ Run.

    Args:
      conf: Redable object consists of conf file.
      halt: If True, shutdown the VM this program running on.
      unzip: If True and downloaded files are zipped, unzip them.
    """
    try:
        # Loading conf.
        obj = yaml.load(conf)

        # Prepare sources.
        if SOURCE in obj:
            source(obj[SOURCE])

        # Prepare data.
        if DATA in obj:
            for url in obj[DATA]:
                LOGGER.info("Loading %s", url)
                download(url, unzip)

        # Run command.
        for i, com in enumerate(obj[RUN]):
            with open(TEMPPATH.format(i), "w") as fp:
                LOGGER.info("Running %s", com)
                execute(com, fp)

        # Upload results.
        dest = obj[RESULT][DESTINATION]
        LOGGER.info("Uploading stdout.")
        upload(TEMPPATH.format("*"), dest)
        if PATTERN in obj[RESULT]:
            for pat in obj[RESULT][PATTERN]:
                LOGGER.info("Uploading %s", pat)
                upload(pat, dest)

        # Garbage collection.
        for path in glob.iglob(TEMPPATH.format("*")):
            os.remove(path)

    finally:
        # Shutdown.
        if halt:
            shutdown.shutdown()


def main():
    """ The main function.
    """
    parser = argparse.ArgumentParser(
        description="Read an instruction from STDIN and run programs in that way.")
    parser.add_argument(
        "-c", "--conf", default=sys.stdin, type=argparse.FileType("r"),
        help="Specify an instruction YAML file instead of STDIN.")
    parser.add_argument(
        "--no-shutdown", default=True, action="store_false", dest="halt",
        help="Not shutdown after finishing tasks."
    )
    parser.add_argument(
        "--no-unzip", default=True, action="store_false", dest="unzip",
        help="Not unzip zipped files."
    )

    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
    finally:
        logging.shutdown()
