# kci builder

## Getting started

`sh build.sh` (can take a while, but build a base Docker image)

`wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.8.tar.xz` (example)
`python3 magicscript.py gcc-8 5.8` (5.8 corresponds to linux-5.8 and we assume there is a tar.xz in the local folder)

you should get an image:
`tuxml-kci-gcc-8:kv5.8` that contains everything (kci, tuxml-kci, kernel source)

and then `docker run -it tuxml-kci-gcc-8:kv5.8 python3 tuxml_kci.py --config tinyconfig`

it should give someting like:
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
