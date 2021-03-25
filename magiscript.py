import errno
import os
import yaml
import argparse
import docker
from docker.errors import APIError
import subprocess


volume_name = "shared_volume"
config_path = "configs"
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

    container_name = f"tuxml-kci-{b_env}_{arch}"
    print(f"Building image for {container_name}")
    docker_client.images.build(path=path, tag=f"{container_name}:latest", nocache=True, forcerm=True)


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
                                                       volumes=f'/{volume_name}',
                                                       host_config=binding_config,
                                                       tty=False,
                                                       stdin_open=False,
                                                       working_dir="/tuxml-kci")
    except APIError:
        # TODO do we really need to force remove here?
        docker_client.api.remove_container(container=container_name, force=True)
        container = docker_client.api.create_container(image=container_name,
                                                       name=container_name,
                                                       volumes=f'/{volume_name}',
                                                       host_config=binding_config,
                                                       tty=False,
                                                       stdin_open=False,
                                                       working_dir="/tuxml-kci")

    docker_client.api.start(container=container.get('Id'))

    # Update local repo of tuxml-kci and build a kernel - USED DURING TEST PHASE SO THAT 'kha_test' IS USED
    command = "git checkout kha_test"
    checkout_cmd = docker_client.api.exec_create(container=container_name, cmd=command)

    command = "git fetch"
    fetch_cmd = docker_client.api.exec_create(container=container_name, cmd=command)

    command = "git pull"
    pull_cmd = docker_client.api.exec_create(container=container_name, cmd=command)
    docker_client.api.exec_start(exec_id=checkout_cmd)
    docker_client.api.exec_start(exec_id=fetch_cmd)
    docker_client.api.exec_start(exec_id=pull_cmd)

    # command = "echo 'yo man' >> /proc/1/fd/1"
    # random_echo_cmd = docker_client.api.exec_create(container=container_name, cmd=command)
    # docker_client.api.exec_start(exec_id=random_echo_cmd, detach=False, tty=True, stream=True)
    #

    command = f"bash -c \"python3 tuxml_kci.py -b {b_env} -k {kver} -a {arch} -c {kconfig} > /proc/1/fd/1\""
    build_cmd = docker_client.api.exec_create(container=container_name, cmd=command)
    docker_client.api.exec_start(exec_id=build_cmd, stream=True, detach=False)

    stop_pattern= "Build of {b_env}_{arch} complete.".format(b_env=b_env, arch=arch)
    for line in docker_client.api.logs(container=container_name, follow=True, stdout=True, stderr=True, stream=True, tail=5, timestamps=True):
        print(line.decode('UTF-8').strip())
        if stop_pattern in line.decode('UTF-8').strip():
            break

    docker_client.api.stop(container=container_name)

if __name__ == '__main__':

    print("Starting...")

    # Check that the correct parameters have been correctly provided
    parser = argparse.ArgumentParser()

    subparser = parser.add_subparsers()

    # Setting parameters requirement for build command
    parser_build = subparser.add_parser('build')
    parser_build.set_defaults(which='build')
    parser_build.add_argument("-b", "--build_env", required=True,
                              help="Select a build environment. Only gcc-x (x is the "
                                   "desired version) is supported.")
    parser_build.add_argument("-a", "--arch", required=True, help="Select an architecture. Supported architectures are "
                                                                  "x86_64, riscv64, mips, arm and arm64.")
    # Setting parameters requirement for run command
    parser_run = subparser.add_parser('run')
    parser_run.set_defaults(which='run')
    parser_run.add_argument("-b", "--build_env", required=True,
                            help="Select a build environment. Only gcc-x (x is the "
                                 "desired version) is supported.")
    parser_run.add_argument("-a", "--arch", required=True, help="Select an architecture. Supported architectures are "
                                                                "x86_64, riscv64, mips, arm and arm64.")
    parser_run.add_argument("-k", "--kversion", required=True, help="Select a linux kernel version. A tarball will be "
                                                                    "downloaded (and cached) and used for building the "
                                                                    "kernel.")
    #parser_run.add_argument("-c", "--config", required=True, help="Select the configuration to be used during the "
    #                                                              "compilation of the kernel.")
    second_subparser = parser_run.add_subparsers()
    parser_label = second_subparser.add_parser("label")
    parser_label.set_defaults(which="label")
    parser_label.add_argument("-l", "--label", required=True,
                              help="Select the label of the configuration to be used during the compilation of the "
                                   "kernel.")

    parser_config = second_subparser.add_parser("config")
    parser_config.set_defaults(which="config")
    parser_config.add_argument("-c", "--config", required=True,
                               help="Select the path of the configuration file to be used during the compilation of "
                                    "the kernel.")

    args = vars(parser.parse_args())


    # Check if the base image exists
    if not docker_client.api.images(name="kci_base"):
        print("The base image is missing.")
        print("Please build the base image first with -->> docker build -t kci_base:latest base/ --no-cache")
        print("This operation must be done only once. Once the base image is available in your system, you won't need to be rebuilt.")
    else:
        print("image: kci_base found...")
        # Populate local dictionary with dependencies list that needs to be written in the Dockerfile
        get_dependencies()

        # Check if the building environment is supported, otherwise stop execution
        if args['build_env'].split('-')[0] in dependencies_data['supported_envs']:

            # Create shared directory between containers. This will used to store generated Dockerfiles and output data
            try:
                os.makedirs(name=volume_name, exist_ok=True)
                os.makedirs(name=volume_name+"/"+config_path, exist_ok=True)
            except OSError as err:
                print(err)

            # If the directory is already existing, check if it contains already the image that we need to build
            dir_content = os.listdir(volume_name)
            build_image_name = "{b_env}_{arch}".format(b_env=args['build_env'], arch=args['arch'])

            # Test which sub command has been entered and act accordingly
            if args.get('which') == 'build':
                if docker_client.api.images(name=build_image_name):
                    print(f"Image for {build_image_name} exists already.")
                    print(f"The old image will be deleted and a new version will be created.")
                build_image(args['build_env'], args['arch'])

            if args.get('which') == 'label':
                print(f"Starting background build inside '{build_image_name}' container.")
                print(f"Results will be available shortly in the following path -> '{volume_name}/{build_image_name}'")
                run_dockerfile(args['build_env'], args['arch'], args['kversion'], args['label'])

            if args.get('which') == "config":
                print(f"Moving {args['config']} to {volume_name}/{config_path}/{args['build_env']}_{args['arch']}.config")
                subprocess.call(f"cp {args['config']} ./{volume_name}/{config_path}/{args['build_env']}_{args['arch']}.config", shell=True)
                run_dockerfile(args['build_env'], args['arch'], args['kversion'], f"./{volume_name}/{config_path}/{args['build_env']}_{args['arch']}.config")