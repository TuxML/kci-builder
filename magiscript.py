import errno
import os
import yaml
import argparse
import docker
from docker import utils, types
from docker.errors import ContainerError, APIError

volume_name = "shared_volume"
dependencies_data = {}
docker_client = docker.from_env()


def get_dependencies():
    global dependencies_data
    with open('deps.yaml') as deps_file:
        dependencies_data = yaml.load(deps_file, yaml.FullLoader)


def build_image(b_env, arch):
    # create a directory containing the Dockerfile (this same directory will contain future metadata)
    path = f"{volume_name}/{b_env}_{arch}"

    try:
        # All newly created folders will be inside $volume_name
        os.mkdir(path)

        # So go the selected folder and produce a dockerfile inside of it
        create_dockerfile(path, b_env, arch)
    except OSError as err:
        if err.errno != errno.EEXIST:
            print(err)
    pass

    container_name = f"tuxml-kci-{b_env}_{arch}"
    print(f"Building image for {container_name}")
    docker_client.images.build(path=path, tag=f"{container_name}:latest", nocache=True)


def create_dockerfile(path, b_env, arch):
    # Retrieve just the version number of gcc, this will be the only thing affecting dependencies installation
    b_env_ver = b_env.split('-')[1]
    with open(path + "/Dockerfile", mode="w") as df:
        df.write("FROM kci_base\n")
        df.write(dependencies_data['arch'][arch].format(b_env_ver=b_env_ver))
        df.write("RUN git clone https://github.com/TuxML/tuxml-kci.git\n")


def run_dockerfile(b_env, arch, kver, kconfig):
    local_shared_volume = os.getcwd() + "/" + volume_name
    container_name = f"tuxml-kci-{b_env}_{arch}"

    # Start a container that will launch kernel building. Destroy content when exiting.
    # Prepare configuration environment and create a container

    binding_config = docker_client.api.create_host_config(binds={f"{local_shared_volume}/": {
        'bind': f"/{volume_name}",
        'mode': 'rw'}
    }
    )

    try:
        container = docker_client.api.create_container(image=container_name,
                                                       name=container_name,
                                                       detach=True,
                                                       volumes=f'/{volume_name}',
                                                       host_config=binding_config,
                                                       working_dir="/tuxml-kci")
    except APIError:
        # TODO do we really need to force remove here?
        docker_client.api.remove_container(container=container_name, force=True)
        container = docker_client.api.create_container(image=container_name,
                                                       name=container_name,
                                                       detach=True,
                                                       volumes=f'/{volume_name}',
                                                       host_config=binding_config,
                                                       working_dir="/tuxml-kci")

    docker_client.api.start(container=container.get('Id'))

    # Update local repo of tuxml-kci and build a kernel - USED DURING TEST PHASE SO THAT 'kha_test' IS USED
    command = "git checkout kha_test"
    checkout_cmd = docker_client.api.exec_create(container=container_name, cmd=command)

    command = "git fetch"
    fetch_cmd = docker_client.api.exec_create(container=container_name, cmd=command)

    command = "git pull"
    pull_cmd = docker_client.api.exec_create(container=container_name, cmd=command)
    docker_client.api.exec_start(exec_id=checkout_cmd, detach=True)
    docker_client.api.exec_start(exec_id=fetch_cmd, detach=True)
    docker_client.api.exec_start(exec_id=pull_cmd, detach=True)

    command = f"python3 tuxml_kci.py -b {b_env} -k {kver} -a {arch} -c {kconfig}"
    build_cmd = docker_client.api.exec_create(container=container_name, cmd=command)
    docker_client.api.exec_start(exec_id=build_cmd, stream=True)


if __name__ == '__main__':

    print("Starting...")

    # Check that the correct parameters have been correctly provided
    parser = argparse.ArgumentParser()

    subparser = parser.add_subparsers()

    # Setting parameters requirement for build command
    parser_build = subparser.add_parser('build')
    parser_build.add_argument("-b", "--build_env", required=True,
                              help="Select a build environment. Only gcc-x (x is the "
                                   "desired version) is supported.")
    parser_build.add_argument("-a", "--arch", required=True, help="Select an architecture. Supported architectures are "
                                                                  "x86_64, riscv64, mips, arm and arm64.")
    # Setting parameters requirement for run command
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
            os.makedirs(name=volume_name, exist_ok=True)
        except OSError as err:
            print(err)

        # If the directory is already existing, check if it contains already the image that we need to build
        dir_content = os.listdir(volume_name)
        dir_lookup = "{b_env}_{arch}".format(b_env=args['build_env'], arch=args['arch'])

        # TODO find a better way to do this
        if len(args) == 2:
            build_image(args['build_env'], args['arch'])
        else:
            print(f"image for {dir_lookup} exists already")
            print("Running container...")
            run_dockerfile(args['build_env'], args['arch'], args['kversion'], args['config'])
