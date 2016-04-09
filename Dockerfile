#
# Dockerfile
#
# Copyright (c) 2015-2016 Junpei Kawamoto
#
# This software is released under the MIT License.
#
# http://opensource.org/licenses/mit-license.php
#
FROM ubuntu:latest
MAINTAINER Junpei Kawamoto <kawamoto.junpei@gmail.com>

# Install packages.
ENV TERM vt100
RUN apt-get update && \
    apt-get install -y unzip libssl-dev python-pip python-dev libffi-dev && \
    apt-get upgrade -y && apt-get clean && \
    rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/
RUN pip install -U pip pip-tools

## Install python packages.
ADD ./requirements.in ./
RUN pip-compile && \
    pip install -r requirements.txt && \
    rm requirements.in requirements.txt

## Install gsutil.
ADD https://storage.googleapis.com/pub/gsutil.tar.gz /tmp
RUN tar -zxvf /tmp/gsutil.tar.gz -C /usr/local
ENV PATH $PATH:/usr/local/gsutil
RUN echo "[GoogleCompute]\nservice_account = default\n[GSUtil]\nparallel_composite_upload_threshold" >> /etc/boto.cfg

# Copy entrypoint
COPY bin /root
WORKDIR /data

# Change working directory
ENTRYPOINT ["/root/entrypoint.sh"]
