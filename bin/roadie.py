#! /usr/bin/env python
#
# roadie.py
#
# Copyright (c) 2015-2016 Junpei Kawamoto
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
APT = "apt"
SOURCE = "source"
DATA = "data"
RUN = "run"
RESULT = "result"
UPLOAD = "upload"

LOGGER = logging.getLogger(__name__)


def apt(conf):
    """ Install packages via apt-get.

    Args:
      conf: list of packages.
    """
    proc = subprocess.Popen(
        ["apt-get", "update"], stdout=sys.stdout, stderr=sys.stderr)
    proc.communicate()

    proc = subprocess.Popen(
        ["apt-get", "install", "-y"] + conf, stdout=sys.stdout, stderr=sys.stderr)
    proc.communicate()


def source(conf, cwd=None):
    """ Prepare source files from git, dropbox, gs, and/or web.

    Args:
      conf: url of a source repository.
      cwd: working directory. (Default: current directory)
    """
    if not cwd:
        cwd = "."

    if conf.endswith(".git"):
        proc = subprocess.Popen(
            ["git", "clone", conf, "."],
            cwd=cwd, stdout=sys.stdout, stderr=sys.stderr)
        proc.communicate()

    else:
        download(conf)

    pkg = os.path.join(cwd, "requirements.in")
    if os.path.exists(pkg):
        proc = subprocess.Popen(
            ["pip-compile", pkg], stdout=sys.stdout, stderr=sys.stderr)
        proc.communicate()

    pkg = os.path.join(cwd, "requirements.txt")
    if os.path.exists(pkg):
        proc = subprocess.Popen(
            ["pip", "install", "-r", pkg], stdout=sys.stdout, stderr=sys.stderr)
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
        ["gsutil", "-m", "cp", pat, dest], stdout=sys.stdout, stderr=sys.stderr)
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

        # Prepare packages.
        if APT in obj:
            LOGGER.info("Installing apt packages.")
            apt(obj[APT])

        # Prepare sources.
        if SOURCE in obj:
            LOGGER.info("Downloading source files.")
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
        dest = obj[RESULT]
        if not dest.endswith("/"):
            dest += "/"
        LOGGER.info("Uploading stdout.")
        upload(TEMPPATH.format("*"), dest)
        if UPLOAD in obj:
            for pat in obj[UPLOAD]:
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
        sys.exit(-1)
    except Exception as e: # pylint: disable=broad-except
        logging.exception("Error")
        sys.exit(1)
    finally:
        logging.shutdown()
