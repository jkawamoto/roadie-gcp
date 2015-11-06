#! /usr/bin/env python
import glob
import os
import subprocess
import sys
import yaml

from downloader import download


TEMPPATH = "/tmp/stdout{0}.txt"
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
def run(conf):
    """ Run.

    Args:
      conf: Redable object consists of conf file.
    """
    obj = yaml.load(conf)

    # Prepare data.
    if "data" in obj:
        for url in obj["data"]:
            download(url)

    # Run command.
    for i, com in enumerate(obj["run"]):
        with open(TEMPPATH.format(i), "w") as fp:
            execute(com, fp)

    # Upload results.
    dest = obj["result"]["destination"]
    upload(TEMPPATH.format("*"), dest)
    for pat in obj["result"]["pattern"]:
        upload(pat, dest)

    # Garbage collection.
    for path in glob.iglob(TEMPPATH.format("*")):
        os.remove(path)


def main():
    """ The main function.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "conf", nargs="+", default=sys.stdin, type=argparse.FileType("w")
        help="")

    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
