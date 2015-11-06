#! /usr/bin/env python
import os
import subprocess
import sys
import yaml

from downloader import download


TEMPPATH = "/tmp/stdout{0}.txt"
def run(command, step=1):
    """ Run a given command.

    Args:
      command: a string specifying command to be run.
      step: step number used for files saving stdout.
    """
    # Does tail work to watch stdout to logging service?
    with open(TEMPPATH.format(step), "w") as stdout:
        p = subprocess.Popen(
            command, shell=True, stdout=stdout, stderr=sys.stdout)
        p.wait()


def main():
    with open("test.yml") as fp:
        obj = yaml.load(fp)
        print obj

        for url in obj["data"]:
            download(url)

        for i, com in enumerate(obj["run"]):
            run(com, i + 1)


if __name__ == "__main__":
    main()
