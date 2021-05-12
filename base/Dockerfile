FROM debian:buster

ARG DEBIAN_FRONTEND=noninteractive

# Install only necessary libraries
RUN apt-get update && apt-get install --no-install-recommends -y procps

# SSL / HTTPS support
RUN apt-get update && apt-get install --no-install-recommends -y \
    apt-transport-https \
    ca-certificates

# Host build tools
RUN apt-get update && apt-get install --no-install-recommends -y \
    bash \
    bc \
    bison \
    bsdmainutils \
    ccache \
    cpio \
    flex \
    g++ \
    gcc \
    git \
    kmod \
    libssl-dev \
    libelf-dev \
    lzop \
    make \
    rsync \
    ssh \
    tar \
    u-boot-tools \
    wget \
    xz-utils

# Python 3
RUN apt-get update && apt-get install --no-install-recommends -y \
    python3 \
    python3-dev \
    python3-venv \
    python3-wheel \
    python3-jinja2 \
    python3-keyring \
    python3-pyelftools \
    python3-setuptools \
    python3-requests \
    python3-yaml \
    python3-pip

RUN pip3 install psutil

RUN pip3 install distro

RUN pip3 install kernelci

RUN echo 'deb http://deb.debian.org/debian testing main' >> /etc/apt/sources.list

