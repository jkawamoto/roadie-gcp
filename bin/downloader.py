#
# downloader.py
#
# Copyright (c) 2015 Junpei Kawamoto
#
# This software is released under the MIT License.
#
# http://opensource.org/licenses/mit-license.php
#
""" Download objects from several services.
"""
import os
import subprocess
import sys
import urlparse


def curl(url, dest):
    """ Download an object using curl.

    Args:
      url: Url specifying an object.
      dest: Destination path.

    Returns:
      Downloaded filename.
    """
    p = subprocess.Popen(
        ["curl", "-O", urlparse.urlunparse(url)], stdout=sys.stdout, cwd=dest)
    p.wait()

    return dest + url.path[url.path.rfind("/"):]


def gsutil(url, dest):
    """ Download an object using gsutil.

    Args:
      url: Url specifying an object.
      dest: Destination path.

    Returns:
      Downloaded filename.
    """
    p = subprocess.Popen(
        ["gsutil", "cp", urlparse.urlunparse(url), dest], stdout=sys.stdout)
    p.wait()

    return dest + url.path[url.path.rfind("/"):]


def dropbox(url, dest):
    """ Download an object from dropbox.

    Args:
      url: Url specifying an object.
      dest: Destination path.

    Returns:
      Downloaded filename.
    """
    new_url = "https://{host}{path}?dl=1".format(host=url.netloc, path=url.path)
    filename = url.path[url.path.rfind("/"):]
    if filename.find(".") == -1:
        filename += ".zip"
    filepath = dest + filename
    p = subprocess.Popen(
        ["wget", new_url, "-O", filepath], stdout=sys.stdout)
    p.wait()

    return filepath


def download(url):
    """ Download an object specified by a url.

    Url can has a destination path. The format is
      scheme://host/path
      scheme://host/path:dest
    where dest is the destination path.

    Scheme is one of http, https, gs, dropbox.

    Args:
      url: An extended url specifying the url of an object and an destination path.
    """
    # Check the url contains a destination path.
    dest = "."
    if url.find(":") != url.rfind(":"):
        dest = url[url.rfind(":")+1:]
        url = url[:url.rfind(":")]

    url = urlparse.urlparse(url)

    downloader = curl
    if url.scheme == "gs":
        downloader = gsutil

    elif url.scheme == "dropbox":
        downloader = dropbox

    path = downloader(url, dest)

    # If donloaded file is a zip, unzip and remove it.
    if path.endswith(".zip"):
        p = subprocess.Popen(
            ["unzip", "-o", path], stdout=sys.stdout, cwd=dest)
        p.wait()

        os.remove(path)