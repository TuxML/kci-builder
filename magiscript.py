#!usr/bin/env python3
import subprocess
import sys
import tempfile
from time import sleep


def main(b_env):
    print("Starting...")
    # create a temporary directory
    with tempfile.TemporaryDirectory() as directory:
        print('The created temporary directory is %s' % directory)
        path = directory + '\Dockerfile'
        create_dockerfile(path, b_env)
        while 1:
            sleep(1)
        subprocess.call(['docker', 'build', directory])


def create_dockerfile(path, b_env):
    with open(path, mode="x") as df:
        df.write("FROM kci_base\n")
        df.write("RUN apt-get update && apt-get install --no-install-recommends -y %s %s-plugin-dev\n" % (b_env, b_env))
        df.write("RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/%s 500\n" % b_env)
        df.write("RUN apt-get update && apt-get install --no-install-recommends -y libc6-dev libcap-dev libcap-ng-dev libelf-dev libpopt-dev\n")


if __name__ == '__main__':
    build_env = sys.argv[1]
    main(build_env)
