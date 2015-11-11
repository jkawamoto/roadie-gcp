#!/bin/bash
if [[ $# = 0 || $1 = -* ]]; then
  exec /root/roadie.py $@
fi
if [ $1 = shutdown ]; then
  exec /root/shutdown.py
fi
exec $@
