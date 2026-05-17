FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get install -y \
        build-essential \
        cmake \
        git \
        curl \
        jq \
        unzip \
        python3 \
        python3-pip \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY certs/ /usr/local/share/ca-certificates/
RUN update-ca-certificates





