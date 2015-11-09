#! /usr/bin/env python
""" The main module of roadie-gcp.
"""
import argparse
import glob
import os
import subprocess
import shutdown
import sys
import yaml
from downloader import download

# Template path of temporary files.
TEMPPATH = "/tmp/stdout{0}.txt"

# Static variables.
DATA = "data"
RUN = "run"
RESULT = "result"
DESTINATION = "destination"
PATTERN = "pattern"

# TODO: Add logging.
def execute(command, stdout, stderr=sys.stdout):
    """ Run a given command.

    Args:
      command: a string specifying command to be run.
      stdout: Writable object to which stdout of subprocess connects.
      stderr: Writable object to which stderr of subprocess connects.
    """
    # Does tail work to watch stdout to logging service?
    p = subprocess.Popen(
        command, shell=True, stdout=stdout, stderr=stderr)
    p.wait()


def upload(pat, dest):
    """ Upload objects matched to a given pattern.

    Args:
      pat: Pattern of objects to be uploaded.
      dest: Destination URL.
    """
    p = subprocess.Popen(
        ["gsutil", "cp", pat, dest], stdout=sys.stdout)
    p.wait()


# whether runner should stop when getting status codes not 0?
def run(conf, halt):
    """ Run.

    Args:
      conf: Redable object consists of conf file.
      halt: If True, shutdown the VM this program running on.
    """
    obj = yaml.load(conf)

    # Prepare data.
    if DATA in obj:
        for url in obj[DATA]:
            download(url)

    # Run command.
    for i, com in enumerate(obj[RUN]):
        with open(TEMPPATH.format(i), "w") as fp:
            execute(com, fp)

    # Upload results.
    dest = obj[RESULT][DESTINATION]
    upload(TEMPPATH.format("*"), dest)
    if PATTERN in obj[RESULT]:
        for pat in obj[RESULT][PATTERN]:
            upload(pat, dest)

    # Garbage collection.
    for path in glob.iglob(TEMPPATH.format("*")):
        os.remove(path)

    # Shutdown.
    if halt:
        shutdown.shutdown()


def main():
    """ The main function.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "conf", nargs="?", default=sys.stdin, type=argparse.FileType("r"),
        help="Path to a configure YAML file. (default: stdin)")
    parser.add_argument(
        "--no-shutdown", default=True, action="store_false", dest="halt",
        help="Not shutdown after finishing tasks."
        )

    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
