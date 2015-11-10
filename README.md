Roadie-GCP
========
A helper container to execute a program on [Google Cloud Platform](https://cloud.google.com/).

Roadie-GCP
  * downloads necessary files from web and [Google Cloud Storage](https://cloud.google.com/storage/),
  * runs commands,
  * uploads results to Google Cloud Storage.

Instructions for Roadie-GCP are simple YAML documents like
```
data:
  - http://sample.com/run.sh
  - gs://a-project/input/data
run:
  - run.sh data
result:
  destination: gs://a-project/result/
  pattern:
    - "*.out"
```

This example commands Roadie-GCP downloads two files and run a command `run.sh data`, then upload results which have extention `.out` to a bucket in Google Cloud Storage. Finally, Roadie-GCP shutdowns the virtual machine Roadie-GCP is running on.

Run
----
```
usage: roadie.py [-h] [--no-shutdown] [conf]

positional arguments:
  conf           Path to a configure YAML file. (default: stdin)

optional arguments:
  -h, --help     show this help message and exit
  --no-shutdown  Not shutdown after finishing tasks.
```




License
--------
This software is released under the MIT License, see LICENSE.
