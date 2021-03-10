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

> **build the kernel image :** ``python3 magiscript.py build [-h] -b BUILD_ENV -a ARCH``
> 
> **run compilation in a container :** ``python3 magiscript.py run [-h] -b BUILD_ENV -a ARCH -c CONFIG -k KVERSION``  
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

The output metadata from the build will be stored in the same folder as the Dockerfile folder.

Example of metadata result:
```
...
{
    "arch": "x86_64",
    "build_environment": "gcc-8",
    "build_log": "build.log",
    "build_platform": [
        "Linux",
        "56d635cfacc4",
        "5.3.7-301.fc31.x86_64",
        "#1 SMP Mon Oct 21 19:18:58 UTC 2019",
        "x86_64",
        ""
    ],
    "build_threads": 10,
    "build_time": 146.69,
    "compiler": "gcc",
    "compiler_version": "8",
    "compiler_version_full": "gcc (Debian 8.3.0-6) 8.3.0",
    "cross_compile": "",
    "defconfig": "none",
    "defconfig_full": "none",
    "status": "PASS",
    "vmlinux_bss_size": 1421312,
    "vmlinux_data_size": 244608,
    "vmlinux_file_size": 11614872,
    "vmlinux_text_size": 4195646
}
```
