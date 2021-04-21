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

# Python 3.7
RUN apt-get update && apt-get install --no-install-recommends -y \
    python3.7 \
    python3-jinja2 \
    python3-keyring \
    python3-pyelftools \
    python3-setuptools \
    python3-requests \
    python3-yaml \
    python3-pip

# Taken from - https://docs.docker.com/engine/examples/running_ssh_service/#environment-variables
RUN mkdir /var/run/sshd
RUN echo 'root:root' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

# expose 22 for ssh server. 7777 for gdb server. 80 for lava communications.
EXPOSE 22 80 7777

# Create adminuser with password 'password'
RUN useradd -ms /bin/bash admin
RUN echo 'admin:password' | chpasswd

# Upon start, run ssh daemon
CMD ["/usr/sbin/sshd", "-D"]

RUN python3 -m pip install kernelci

RUN python3 -m pip install psutil

RUN python3 -m pip install distro

RUN echo 'deb http://deb.debian.org/debian testing main' >> /etc/apt/sources.list