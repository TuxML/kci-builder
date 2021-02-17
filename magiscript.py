import subprocess
import os
import sys
import tempfile
from random import randint


def main(b_env,):
    print("Starting...")
    # create a temporary directory
    with tempfile.TemporaryDirectory() as directory:
        print('The created temporary directory is %s' % directory)
        path = directory + '/Dockerfile'
        create_dockerfile(path, b_env)
        container_name = b_env + "_" + str(randint(0,1024))
        # TODO FIX THIS THING
        stupid_concat = "docker build --no-cache --tag "+container_name + " ."
        os.chdir(directory)
        subprocess.run(stupid_concat, shell=True)



def create_dockerfile(path, b_env):
    with open(path, mode="x") as df:
        df.write("FROM kci_base\n")
        df.write("RUN apt-get update && apt-get install --no-install-recommends -y %s %s-plugin-dev\n" % (b_env, b_env))
        df.write("RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/%s 500\n" % b_env)
        df.write("RUN apt-get update && apt-get install --no-install-recommends -y libc6-dev libcap-dev libcap-ng-dev libelf-dev libpopt-dev\n")
        df.write("RUN git clone https://github.com/TuxML/tuxml-kci.git\n")
        df.write("RUN python3 tuxml-kci/tuxml_kci.py --kernel_version 5.9 --config defconfig\n")
        df.write("RUN pwd\n")
        df.write("RUN cat tuxml-kci/kernel/build/bmeta.json\n")


if __name__ == '__main__':
    build_env = sys.argv[1]
    main(build_env)
