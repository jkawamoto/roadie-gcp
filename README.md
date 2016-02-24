Roadie-GCP
===========

A helper container to execute a program on [Google Cloud Platform](https://cloud.google.com/).

Roadie-GCP
  * downloads necessary files from web and [Google Cloud Storage](https://cloud.google.com/storage/),
  * runs commands,
  * uploads results to Google Cloud Storage.

Instructions for Roadie-GCP are simple YAML documents like
```
data:
  - http://sample.com/run.sh
  - gs://a-project/input/data:/tmp
run:
  - run.sh /tmp/data
result:
  destination: gs://a-project/result/
  pattern:
    - "*.out"
```

This example commands Roadie-GCP downloads two files and run a command `run.sh /tmp/data`, then upload results which have extention `.out` to a bucket in Google Cloud Storage. Finally, Roadie-GCP shutdowns the virtual machine Roadie-GCP is running on.

Run
----
Letting `conf.yml` be an instruction file,
```
$ docker run -i jkawamoto/roadie-gcp < conf.yml
```
starts Roadie-GCP with the instruction.
You also specify an instruction file insted of STDIN by
```
$ docker run -i jkawamoto/roadie-gcp -c /path/to/conf.yml
```

Roadie-GCP will shutdown your VM after finishing instructions.
Thus, `https://www.googleapis.com/auth/compute` scope is required.
To prevent this behavior, use `--no-shutdown` option.

The full description of arguments is below.
```
usage: docker run -i jkawamoto/roadie-gcp [-h] [-c CONF] [--no-shutdown]

Read an instruction from STDIN and run programs in that way.

optional arguments:
  -h, --help            show this help message and exit
  -c CONF, --conf CONF  Specify an instruction YAML file instead of STDIN.
  --no-shutdown         Not shutdown after finishing tasks.
  --no-unzip            Not unzip zipped files.  
```

Instruction
-------------
An instruction file is a YAML document. It has three top-level elements; `data`, `run`, and `result`.

### data
The `data` section specifies URLs to be downloaded.
It must be a list of extended URLs and the format of extended URL is
```
scheme://hostname/path
```
or
```
scheme://hostname/path:dest
```
URL schemes Roadie-GCP supports are `gs`, `dropbox` and schemes which `curl` supports. To download objects, Roadie-GCP uses `curl` but uses `gsutil` for `gs` scheme. `dropbox` is a pseudo scheme to download objects from [Dropbox](https://www.dropbox.com/). To use this scheme, get public URL from Dropbox and then replace `https` to `dropbox`. When you download objects via Dropbox's public link, they are zipped. Using `dropbox` scheme will unzip those objects.

Downloaded objects will be put in `/data` which is the default working directory.
You can also use the second format of URL to specify destinations of objects.

### run
The `run` section specifies what commands will be run.
It must be a list of commands.
Those commands will be executed via shell.
STDOUT of those commands will be stored to files named `stdout*.txt` and uploaded to Google Cloud Storage.
For example, the outputs of the first commands will be stored to `stdout0.txt`.
On the other hands, STRERR will be outputted to docker logs.

### result
The `result` section specifies where outputted results should be stored.
Outputted results include STDOUT of each commands.
This section consists of two elements.
The first one is `destination` and it specifies a place of Google Cloud Storage. It must be a URL of which scheme is `gs`.
The other element is `pattern` and it consist of a list of glob patterns.
Objects matching to one of the patterns will be uploaded to the cloud storage. Each glob pattern can have a destination after `:`.
For example, `"*.out:result` means objects matching `*.out` will be uploaded to `result` folder.

License
--------
This software is released under the MIT License, see LICENSE.
