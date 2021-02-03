#!usr/bin/env python3
import tempfile


def main():
    print("Starting...")
    # create a temporary directory
    with tempfile.TemporaryDirectory() as directory:
        print('The created temporary directory is %s' % directory)
        create_dockerfile(directory)


def create_dockerfile(path, build_env):
    with open(path+"\Dockerfile", mode="x") as df:
        df.write("FROM kci_base\n")
        df.write("RUN apt-get update && apt-get install --no-install-recommends -y gcc-%d gcc-%d-plugin-dev\n" % (build_env,build_env))
        df.write("RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-%d 500\n" % build_env)
        df.write("RUN apt-get update && apt-get install --no-install-recommends -y libc6-dev libcap-dev libcap-ng-dev libelf-dev libpopt-dev\n")


if __name__ == '__main__':
    main()
