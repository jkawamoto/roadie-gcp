#! /usr/bin/env python
#
# shutdown.py
#
# Copyright (c) 2015 Junpei Kawamoto
#
# This software is released under the MIT License.
#
# http://opensource.org/licenses/mit-license.php
#
""" Shuddown my insance.
"""
import logging
import urllib2
from apiclient import discovery
from auth import Auth

_INSTANCE = "http://169.254.169.254/computeMetadata/v1/instance/"
_PROJECT = "http://169.254.169.254/computeMetadata/v1/project/"


def _get(url):
    """ Create a request object for a given url.

    Args:
      url: requesting url.

    Returns:
      A urllib2.Request object.
    """
    req = urllib2.Request(url)
    req.add_header("Metadata-Flavor", "Google")
    return urllib2.urlopen(req).readline()


def shutdown():
    """ Shutdown the instance where this method is called.
    """
    auth = Auth()
    instance = _get(_INSTANCE + "hostname").split(".")[0]
    zone = _get(_INSTANCE + "zone").split("/")[-1]
    project = _get(_PROJECT + "project-id")

    logging.info("Instance %s will be shut down.", instance)

    sp = discovery.build("compute", "v1")
    req = sp.instances().delete(project=project, zone=zone, instance=instance)
    req.headers["Authorization"] = auth.header_str()
    req.execute()


def main():
    """ The main function.
    """
    shutdown()


if __name__ == "__main__":
    main()
