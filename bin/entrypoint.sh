#!/bin/bash
#
# entrypoint.sh
#
# Copyright (c) 2015 Junpei Kawamoto
#
# This software is released under the MIT License.
#
# http://opensource.org/licenses/mit-license.php
#
export PATH=$PATH:`pwd`
if [[ $# = 0 || $1 = -* ]]; then
  exec /root/roadie.py $@
fi
if [ $1 = shutdown ]; then
  exec /root/shutdown.py
fi
exec $@
