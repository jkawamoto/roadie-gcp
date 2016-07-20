Roadie-GCP
===========
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
[![Build Status](https://travis-ci.org/jkawamoto/roadie-gcp.svg?branch=master)](https://travis-ci.org/jkawamoto/roadie-gcp)
[![Code Climate](https://codeclimate.com/github/jkawamoto/roadie-gcp/badges/gpa.svg)](https://codeclimate.com/github/jkawamoto/roadie-gcp)
[![Dockerhub](https://img.shields.io/badge/dockerhub-jkawamoto%2Froadie--gcp-blue.svg)](https://hub.docker.com/r/jkawamoto/roadie-gcp/)
[![Japanese](https://img.shields.io/badge/qiita-%E6%97%A5%E6%9C%AC%E8%AA%9E-brightgreen.svg)](http://qiita.com/jkawamoto/items/fbe28dbed533a7001f68)

A helper container to execute a program on [Google Cloud Platform](https://cloud.google.com/).

Roadie-GCP
  * downloads necessary files from web and [Google Cloud Storage](https://cloud.google.com/storage/),
  * runs commands,
  * uploads results to Google Cloud Storage.

Instructions for Roadie-GCP are simple YAML documents like

```yaml
apt:
- nodejs
source: https://github.com/itslab-kyushu/youtube-comment-scraper.git
data:
- http://sample.com/run.sh
- gs://a-project/input/data:/tmp
run:
- npm install
- run.sh /tmp/data
result: gs://a-project/result/
upload:
- "*.out"
```

This example commands Roadie-GCP to install `nodejs` via apt,
and download source codes from a Github repository. Then,
it prepares to data from some web server and Google Cloud Storage,
and run a command `run.sh /tmp/data`.
Finally, it uploads stdout and results which have extension `.out` to a bucket in Google Cloud Storage.
Roadie-GCP automatically shutdowns the virtual machine Roadie-GCP is running on, so you can minimize charge.

Run
----
Letting `conf.yml` be an instruction file,

```sh
$ docker run -i jkawamoto/roadie-gcp < conf.yml
```
starts Roadie-GCP with the instruction.
You also specify an instruction file instead of STDIN by

```sh
$ docker run -i jkawamoto/roadie-gcp -c /path/to/conf.yml
```

Roadie-GCP will shutdown your VM after finishing instructions.
Thus, `https://www.googleapis.com/auth/compute` scope is required.
To prevent this behavior, use `--no-shutdown` option.

The full description of arguments is below.

~~~
usage: docker run -i jkawamoto/roadie-gcp [-h] [-c CONF] [--no-shutdown]

Read an instruction from STDIN and run programs in that way.

optional arguments:
  -h, --help            show this help message and exit
  -c CONF, --conf CONF  Specify an instruction YAML file instead of STDIN.
  --no-shutdown         Not shutdown after finishing tasks.
  --no-unzip            Not unzip zipped files.  
~~~

Instruction
-------------
An instruction file is a YAML document. It has three top-level elements;
`apt`, `source`, `data`, `run`, `result`, and `upload`.

### apt
The `apt` section specifies a package list to be installed via apt.

```yaml
apt:
- nodejs
- package_a
- package_b
```


### souce
The `source` section specifics how to obtain source codes.
It could have either git repository URL or normal URL.
A git repository URL is a URL ends with `.git`.
Such URLs will be used with `git clone`.
If you want to use ssh to connect your repository,
you may need to deploy valid ssh keys in `/root/.ssh` in this container.
For *normal URL*, in addition to the basic scheme `http` and `https`,
this url supports `gs` which means an object in Google Cloud Storage, and `dropbox`.
See the next section for detail.

#### Example
##### Clone source code from a git repository:
```yaml
source: https://github.com/itslab-kyushu/youtube-comment-scraper.git
```

##### Download source code from some web server:
```yaml
source: https://exmaple.com/abc.txt
```

##### Download source code from Google Cloud Storage:
```yaml
source: gs://your_bucket/path_to_object
```

##### Download source code from Dropbox:
```yaml
source: dropbox://www.dropbox.com/sh/abcdefg/ABCDEFGHIJKLMN
```

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
Roadie-GCP supports only a place in Google Cloud Storage, currently.
Thus, the value of the `result` element must be a URL of which scheme is `gs`.

### upload
The `upload` section specifies other files to be uploaded as results.
This section consist of a list of glob patterns.
Objects matching to one of the patterns will be uploaded to the cloud storage. Each glob pattern can have a destination after `:`.
For example, `"*.out:result` means objects matching `*.out` will be uploaded to `result` folder.

License
--------
This software is released under the MIT License, see [LICENSE](LICENSE).
