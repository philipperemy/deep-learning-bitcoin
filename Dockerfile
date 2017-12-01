FROM ubuntu:16.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    git \
    python3-tk \
    python3-pip \
    python3-dev

COPY requirements.txt /tmp/

RUN cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip \
  && pip install --requirement /tmp/requirements.txt

VOLUME ["/app"]
WORKDIR "/app"

RUN /bin/bash
