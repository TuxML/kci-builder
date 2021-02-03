FROM kci_base

RUN apt-get update && apt-get install --no-install-recommends -y \
    gcc-8 \
    gcc-8-plugin-dev

RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 500

# kselftest
RUN apt-get update && apt-get install --no-install-recommends -y \
   libc6-dev \
   libcap-dev \
   libcap-ng-dev \
   libelf-dev \
   libpopt-dev

RUN cd /kernelci-core && ./kci_build update_mirror --build-config=next --mirror=linux-mirror.git \
    && ./kci_build update_repo --build-config=next --kdir=linux --mirror=linux-mirror.git \
    && ./kci_build build_kernel --defconfig=defconfig --arch=x86_64 --build-env=gcc-8 --kdir=linux
