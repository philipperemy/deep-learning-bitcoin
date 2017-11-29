FROM ubuntu:16.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    git

RUN apt-get update \
  && apt-get install -y --no-install-recommends python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip \
  && pip install numpy pandas

VOLUME ["/app"]
WORKDIR "/app"

RUN /bin/bash
