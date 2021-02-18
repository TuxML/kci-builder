# kci builder

## Getting started

`sh build.sh` (can take a while, but build a base Docker image)

`python3 magicscript.py gcc-8` 

it should give someting like:
```
...
Extracting 5.9.tar.xz.
5.9.tar.xz has been extracted into linux-5.9
Cleaning the source code . . .
Trying to make tinyconfig into /tuxml-kci/kernel
/tuxml-kci
/kernelci-core

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
Removing intermediate container 56d635cfacc4
 ---> 3d2b101f5477
Successfully built 3d2b101f5477
Successfully tagged gcc-8_247:latest
```
