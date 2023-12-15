Gazprombank AI-chat for hackaton

<b>Setup</b>
1. Clone repository
```bash
git clone https://github.com/unnamedAniki/masks.git
```
2. Install venv
```bash
python3 -m venv venv
```
3. Activate venv
```bash
source venv/bin/activate
```
4. Install requirements
```bash
pip install -r requirements.txt
```
5. Run server
```bash
./main.py server run
```
<b>Llama model setup for using nvidia GPU</b>

Make sure you already installed Cmake and cuda toolkit

>Needed links below:
>[CUDA toolkit install guide link](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/contents.html)
>[cmake install guide link](https://geeksww.com/tutorials/operating_systems/linux/installation/downloading_compiling_and_installing_cmake_on_linux.php)

1. Create env vars CMAKE_ARGS and FORCE_CMAKE
```bash
CMAKE_ARGS="-DLLAMA_CUBLAS=on"
```
2. reinstall llama python package in venv(!!!) 
```bash
pip install llama-cpp-python --no-cache-dir --force-reinstall --verbose
```
>use `verbose` to output full installation info
