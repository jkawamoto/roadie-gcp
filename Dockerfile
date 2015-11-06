#
# Dockerfile
#
# Copyright (c) 2015 Junpei Kawamoto
#
# This software is released under the MIT License.
#
# http://opensource.org/licenses/mit-license.php
#
FROM ubuntu:latest
MAINTAINER Junpei Kawamoto <kawamoto.junpei@gmail.com>

# Install packages
ENV TERM vt100
RUN apt-get update && \
    apt-get install -y curl wget unzip libssl-dev python-pip \
            python-dev libffi-dev python-crypto python-openssl
RUN pip install -U google-api-python-client gsutil pyyaml
RUN echo "[GoogleCompute]\nservice_account = default" >> /etc/boto.cfg

# Copy entrypoint
COPY bin /root
WORKDIR /data

# Change working directory
ENTRYPOINT ["/root/roadie.py"]
