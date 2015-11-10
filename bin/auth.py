#
# auth.py
#
# Copyright (c) 2015 Junpei Kawamoto
#
# This software is released under the MIT License.
#
# http://opensource.org/licenses/mit-license.php
#
""" Run an authenticate protocol.
"""
import json
import urllib2

_METADATA_SERVER = "http://169.254.169.254/computeMetadata/v1/instance/service-accounts"
_SERVICE_ACCOUNT = "default"


class Auth(object):
    """ Manage auth credentials.
    """

    def __init__(self):
        self.execute()

    def execute(self):
        """ Run an authentication protocol to obtain a credential.
        """
        req = urllib2.Request("{0}/{1}/token".format(_METADATA_SERVER, _SERVICE_ACCOUNT))
        req.add_header("Metadata-Flavor", "Google")

        data = json.load(urllib2.urlopen(req))

        self._token = data["access_token"]
        self._type = data["token_type"]

    def header_str(self):
        """ Make a header string for HTTP.
        """
        return "{0} {1}".format(self.type, self.token)

    @property
    def token(self):
        """ Token.
        """
        return self._token

    @property
    def type(self):
        """ Token type.
        """
        return self._type
