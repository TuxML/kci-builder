python3 magiscript.py build -b gcc-8 -a x86_64

python3 magiscript.py run -b gcc-8 -a x86_64 -k 5.0 label -l tinyconfig

./kci_test generate \
  --bmeta-json=/shared_volume/gcc-8_x86_64/1616596107_4.13/_install_/bmeta.json \
  --dtbs-json=/shared_volume/gcc-8_x86_64/1616596107_4.13/_install_/dtbs.json \
  --plan=baseline_qemu \
  --target=qemu_x86_64 \
  --user=admin \
  --lab-config=lab-local \
  --lab-token=8ec4c0aeaf934ed1dce98cdda800c81c \
  --storage=http://storage/ \
  > job_docker.yaml

lab-local:
  lab_type: lava
  url: 'http://master1'
  filters:
    - passlist:
        plan:
          - baseline

./kci_test submit \
  --user=admin \
  --lab-config=lab-local \
  --lab-token=8ec4c0aeaf934ed1dce98cdda800c81c \
  --jobs=job_docker.yaml

Manque : 
  - kernel.tree
  - kernel.version
  - git.commit
  - git.describe
  - git.branch
  - git.url
   to submit

```python
local_shared_volume = os.getcwd() + "/" + volume_name
    container_name = f"tuxml-kci-{b_env}_{arch}"

    # If a lava-lab is not running then launch one

    if  (docker_client.containers.get("local_master1_1").status == 'running') == True:
        print("A Lava instance is already running")
    else:
        print("No lava running...")
        os.system("rm -rf lava_kci/output")
        back = os.getcwd()
        os.chdir("lava_kci/")
        os.system("python3 lavalab-gen.py")
        os.chdir(back)
        os.system("docker-compose -f lava_kci/output/local/docker-compose.yml up -d")
        print("Lava now launch.")
```

After get container ID
```python
# Connect the container to the Lava network
    os.system(f"docker network connect local_default {container.get('Id')}")
```