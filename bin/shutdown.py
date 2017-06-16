#! /usr/bin/env python
#
# shutdown.py
#
# Copyright (c) 2015-2017 Junpei Kawamoto
#
# This software is released under the MIT License.
#
# http://opensource.org/licenses/mit-license.php
#
"""Shutdown my insance.
"""
# pylint: disable=invalid-name
import logging
import sys
import urllib2
from apiclient import discovery  # pylint: disable=import-error
from auth import Auth

_INSTANCE = "http://169.254.169.254/computeMetadata/v1/instance/"
_PROJECT = "http://169.254.169.254/computeMetadata/v1/project/"

LOGGER = logging.getLogger(__name__)


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

    Returns:
      True if there are no errors.
    """
    try:
        auth = Auth()
        instance = _get(_INSTANCE + "hostname").split(".")[0]
        zone = _get(_INSTANCE + "zone").split("/")[-1]
        project = _get(_PROJECT + "project-id")

        LOGGER.info("Instance %s will be shut down.", instance)

        sp = discovery.build("compute", "v1", cache_discovery=False)
        req = sp.instances().delete(  # pylint: disable=no-member
            project=project, zone=zone, instance=instance)
        req.headers["Authorization"] = auth.header_str()

        req.execute()
        return True

    except urllib2.URLError as e:
        LOGGER.warning("Shutdown was interrupted. (%s)", e)
        return False


def main():
    """ The main function.

    Returns:
      True if there are no errors.
    """
    return shutdown()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    try:
        if not main():
            sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)
    finally:
        logging.shutdown()
