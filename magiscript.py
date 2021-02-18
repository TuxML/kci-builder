import subprocess
import os
import sys
import tempfile
from random import randint


def main(b_env, kversion):
    print("Starting...")
    # create a temporary directory
    path = './Dockerfile'
    create_dockerfile(path, b_env, kversion)
    container_name = "tuxml-kci-" + b_env
    # TODO FIX THIS THING
    stupid_concat = "docker build --no-cache --tag " + container_name + ":" + "kv" + kversion + " ."
    subprocess.run(stupid_concat, shell=True)



def create_dockerfile(path, b_env, kversion):
    with open(path, mode="w") as df:
        df.write("FROM kci_base\n")
        df.write("RUN apt-get update && apt-get install --no-install-recommends -y %s %s-plugin-dev\n" % (b_env, b_env))
        df.write("RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/%s 500\n" % b_env)
        df.write("RUN apt-get update && apt-get install --no-install-recommends -y libc6-dev libcap-dev libcap-ng-dev libelf-dev libpopt-dev\n")
        df.write("RUN git clone https://github.com/TuxML/tuxml-kci.git\n")
        df.write("WORKDIR tuxml-kci/\n")
        df.write("COPY ./linux-" + kversion + ".tar.xz .\n")
        df.write("RUN mkdir -p ./kernel && tar xf linux-" + kversion + ".tar.xz -C ./kernel --strip-components=1 && rm linux-" + kversion + ".tar.xz")
        # df.write("RUN python3 tuxml_kci.py --kernel_version 5.9 --config tinyconfig\n")


if __name__ == '__main__':
    build_env = sys.argv[1]
    kversion = sys.argv[2]
    main(build_env, kversion)
