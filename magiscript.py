import subprocess
import os
import yaml
import argparse

volume_name = "shared_volume"
dependencies_data = {}


def get_dependencies():
    global dependencies_data
    with open('deps.yaml') as deps_file:
        dependencies_data = yaml.load(deps_file, yaml.FullLoader)


def build_image(b_env, arch):
    # create a directory containing the Dockerfile (this same directory will contain future metadata)
    path = "{b_env}_{arch}".format(b_env=b_env, arch=arch)
    dockerfile_name = path + "/Dockerfile"

    try:
        # All newly created folders will be inside "volume_name"
        os.chdir(volume_name)
        os.mkdir(path)

        # So go the selected folder and produce a dockerfile inside of it
        create_dockerfile(dockerfile_name, b_env, arch)
    except OSError as err:
        print(err)

    container_name = "tuxml-kci-%s_%s" % (b_env, arch)
    print("Building image for %s" % container_name)
    command = "docker build -f %s --no-cache --tag %s:latest ." % (dockerfile_name, container_name)
    subprocess.run(command, shell=True)

def list_images():
    command = "docker images | grep tuxml-kci-"
    subprocess.run(command, shell=True )

def create_dockerfile(dockerfile_name, b_env, arch):
    # Retrieve just the version number of gcc, this will be the only thing affecting dependencies installation
    b_env_ver = b_env.split('-')[1]
    with open(dockerfile_name, mode="w") as df:
        df.write("FROM kci_base\n")
        df.write(dependencies_data['arch'][arch].format(b_env_ver=b_env_ver))
        df.write("RUN git clone https://github.com/TuxML/tuxml-kci.git\n")
        df.write("WORKDIR tuxml-kci/\n")


def run_dockerfile(b_env, arch, kver, kconfig):
    current_path = os.getcwd() + "/" + volume_name
    container_name = "tuxml-kci-%s_%s:latest" % (b_env, arch)
    command = "docker run --name %s -d -v %s:/%s %s:latest " % (container_name,current_path, volume_name, container_name)
    subprocess.run(command, shell=True)

    command = "docker exec -d %s git fetch" % container_name
    subprocess.run(command, shell=True)

    command = "docker exec -d %s git pull" % container_name
    subprocess.run(command, shell=True)

    command = "docker exec -d %s python3 tuxml_kci.py --config %s --kernel_version %s" % (container_name, kconfig, kver)
    subprocess.run(command, shell=True)

def create_volume(b_env, arch):
    command = "docker volume create --name %s" % volume_name
    subprocess.run(command, shell=True)


if __name__ == '__main__':

    print("Starting...")

    # Check that the correct parameters have been correctly provided
    parser = argparse.ArgumentParser()

    subparser = parser.add_subparsers()
    parser_build = subparser.add_parser('build')
    parser_build.add_argument("-b", "--build_env", required=True,
                              help="Select a build environment. Only gcc-x (x is the "
                                   "desired version) is supported.")
    parser_build.add_argument("-a", "--arch", required=True, help="Select an architecture. Supported architectures are "
                                                                  "x86_64, riscv64, mips, arm and arm64.")
    parser_run = subparser.add_parser('run')
    parser_run.add_argument("-b", "--build_env", required=True,
                            help="Select a build environment. Only gcc-x (x is the "
                                 "desired version) is supported.")
    parser_run.add_argument("-a", "--arch", required=True, help="Select an architecture. Supported architectures are "
                                                                "x86_64, riscv64, mips, arm and arm64.")
    parser_run.add_argument("-k", "--kversion", required=True, help="Select a linux kernel version. A tarball will be "
                                                                    "downloaded (and cached) and used for building the "
                                                                    "kernel.")
    parser_run.add_argument("-c", "--config", required=True, help="Select the configuration to be used during the "
                                                                  "compilation of the kernel.")

    args = vars(parser.parse_args())

    # Populate local dictionary with dependencies list that needs to be written in the Dockerfile
    get_dependencies()

    # Check if the building environment is supported, otherwise stop execution
    if args['build_env'].split('-')[0] in dependencies_data['supported_envs']:

        # Create shared directory between containers. This will used to store generated Dockerfiles and output data
        try:
            os.mkdir(volume_name)
        except OSError as err:
            print(err)

        # If the directory is already existing, check if it contains already the image that we need to build
        dir_content = os.listdir(volume_name)
        dir_lookup = "{b_env}_{arch}".format(b_env=args['build_env'], arch=args['arch'])

        if len(args) == 2:
            build_image(args['build_env'], args['arch'])
        else:
            print("image for %s exists already" % dir_lookup)
            print("Running container...")
            run_dockerfile(args['build_env'], args['arch'], args['kversion'], args['config'])
