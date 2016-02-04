#
# downloader.py
#
# Copyright (c) 2015-2016 Junpei Kawamoto
#
# This software is released under the MIT License.
#
# http://opensource.org/licenses/mit-license.php
#
""" Download objects from several services.
"""
import contextlib
import os
import re
import shutil
import subprocess
import sys
import urllib2
import urlparse


def _copy_response(res, dest):
    """ Copy a response opened by urllib2 to a destination.

    Args:
      res: Response made by urllib2.urlopen.
      dest: Destination path.
    """
    with open(dest, "wb") as fp:
        shutil.copyfileobj(res, fp)


def curl(url, dest):
    """ Download an object using curl.

    Args:
      url: Parsed URL specifying an object.
      dest: Destination path.

    Returns:
      Path for the downloaded file.
    """
    with contextlib.closing(urllib2.urlopen(urlparse.urlunparse(url))) as res:
        _copy_response(res, dest)

    return dest


def gsutil(url, dest):
    """ Download an object using gsutil.

    Args:
      url: Parsed URL specifying an object.
      dest: Destination path.

    Returns:
      Path for the downloaded file.
    """
    p = subprocess.Popen(
        ["gsutil", "cp", urlparse.urlunparse(url), filename], stdout=sys.stdout)
    p.wait()
    return dest


def dropbox(url, dest):
    """ Download an object from dropbox.

    Args:
      url: Parsed URL specifying an object.
      dest: Destination path.

    Returns:
      Downloaded filename.
    """
    new_url = "https://{host}{path}?dl=1".format(host=url.netloc, path=url.path)

    with contextlib.closing(urllib2.urlopen(new_url)) as res:
        disposition = res.info().getheader("content-disposition")
        match = re.search("filename=\"(.*)\";", disposition)
        if match and match.group(1).endswith(".zip"):
            dest += ".zip"

        _copy_response(res, dest)

    return dest


def download(url):
    """ Download an object specified by a url.

    Url can have a destination path. The format is
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

    # Parse the URL.
    purl = urlparse.urlparse(url)

    # If the destination path is a directory, use filename as same as URL.
    if os.path.isdir(dest) or dest[:-1] == "/":
        dest = os.path.join(dest, purl.path[purl.path.rfind("/")+1:])

    # Choose downloader.
    downloader = curl
    if purl.scheme == "gs":
        downloader = gsutil
    elif purl.scheme == "dropbox":
        downloader = dropbox

    res = downloader(purl, dest)

    # If donloaded file is a zip, unzip and remove it.
    if res.endswith(".zip"):
        p = subprocess.Popen(
            ["unzip", "-o", res], stdout=sys.stdout, cwd=os.path.dirname(res))
        p.wait()
        os.remove(res)
