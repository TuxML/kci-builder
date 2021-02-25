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

> ``python3 magiscript.py [-h] -b BUILD_ENV -a ARCH -k KVERSION``
> 
> Arguments details : 
> 
> `-h` will print a help message
> 
> `-b` BUILD_ENV or `--build-env` BUILD_ENV, must be used with a value to specify the building environment like **gcc-7** or **gcc8**
>
> `-a` ARCH or `--arch` ARCH, must be used with a value to specify the architecture for the build. Available architectures are : x86_64, arm, arm64, mips and riscv64
> 
> `k` KVERSION or `--kversion` KVERSION, must be used with a value to specify the version of the kernel to be downloaded and used for the build

## Example

> ``python3 magiscript.py -b gcc-8 -a x86_64 -k 4.14``

### Remarks
> If the dockerfile for a specific configuration already exists, it will not be created again

## Build the kernel

> Once the image has been created, it should have the following name `tuxml-kci-[BUILD_ENV]_[ARCH]` with the tag `kv[KVERSION]`
> 
> In order to run the container `docker run -it tuxml-kci-[BUILD_ENV]_[ARCH]:kv[KVERSION] python3 tuxml_kci.py --config tinyconfig`

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
