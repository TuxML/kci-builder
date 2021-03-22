# kci builder

## Getting started

> Can take a while, but build a base Docker image that will be used for specific building environment images
> 
> `sh build.sh` 

### Dependencies 
> Please make sure that you have pyyaml installed with 
> 
> `pip3 install pyyaml`
## Script usage

> 1) **build the kernel image :** ``python3 magiscript.py build [-h] -b BUILD_ENV -a ARCH``
> 
> 2) **run compilation in a container :** ``python3 magiscript.py run [-h] -b BUILD_ENV -a ARCH -c CONFIG -k KVERSION``  
> 
> Arguments details : 
>   
> chose `build` if you want to build an image with a specific BUILD_ENV and ARCH 
> 
> chose `run` if an image is already built and you want to compile a kernel for a specific BUILD_ENV, ARCH, CONFIG and KVERSION
> 
> `-h` will print a help message
> 
> `-b` BUILD_ENV or `--build-env` BUILD_ENV, must be used with a value to specify the building environment like **gcc-7** or **gcc8**
>
> `-a` ARCH or `--arch` ARCH, must be used with a value to specify the architecture for the build. Available architectures are : x86_64, arm, arm64, mips and riscv64
> 
> `-c` CONFIG ir `--config` CONFIG, will specify wich type of configuration will be used for the compilation. For example : tinyconfig or defconfig.
> 
> `k` KVERSION or `--kversion` KVERSION, must be used with a value to specify the version of the kernel to be downloaded and used for the build

## Example

> ``python3 magiscript.py build -b gcc-8 -a x86_64``
> 
> ``python3 magiscript.py run -b gcc-8 -a x86_64 -k 4.13 -c tinyconfig``

### Remarks
> If the dockerfile for a specific configuration already exists, it will not be created again

The output metadata from the build will be stored in the same folder as the Dockerfile folder. The path should look like this:

> **kci-builder/shared_volume/[gcc-x_archy]/[timestamp.kver]/**

Example of metadata result: (bmeta.json)
```
...
{
    "arch": "x86_64",
    "build_environment": "gcc-9",
    "build_log": "build.log",
    "build_platform": [
        "Linux",
        "11e16465453f",
        "5.4.72-microsoft-standard-WSL2",
        "#1 SMP Wed Oct 28 23:40:43 UTC 2020",
        "x86_64",
        ""
    ],
    "build_threads": 8,
    "build_time": 157.61,
    "compiler": "gcc",
    "compiler_version": "9",
    "compiler_version_full": "gcc (Debian 9.3.0-22) 9.3.0",
    "cross_compile": "",
    "defconfig": "tinyconfig",
    "defconfig_full": "tinyconfig",
    "dtb_dir": null,
    "file_server_resource": "",
    "git_branch": "",
    "git_commit": "",
    "git_describe": "",
    "git_describe_v": "",
    "git_url": "",
    "job": "",
    "kconfig_fragments": "",
    "kernel_config": "kernel.config",
    "kernel_image": "bzImage",
    "kselftests": null,
    "modules": null,
    "status": "PASS",
    "system_map": "System.map",
    "text_offset": "0x01000000",
    "vmlinux_bss_size": 94208,
    "vmlinux_data_size": 208832,
    "vmlinux_file_size": 3203464,
    "vmlinux_text_size": 667702
}
```
