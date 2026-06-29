FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    wget \
    curl \
    unzip \
    blender \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libegl1 \
    libxi6 \
    libxkbcommon-x11-0 \
    python3-dev \
    python3-setuptools \
    cmake \
    libeigen3-dev \
    libcgal-dev

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniconda3-latest-Linux-x86_64.sh

ENV PATH=/opt/conda/bin:$PATH

RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main

RUN conda create -y -n athena python=3.10

SHELL ["conda","run","-n","athena","/bin/bash","-c"]

RUN pip install --upgrade pip

RUN pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124

COPY requirements.txt /tmp/requirements.txt

RUN sed -i '/^bpy==/d' /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

WORKDIR /workspace

COPY third_party /workspace/Hunyuan3D-2.1

WORKDIR /workspace/Hunyuan3D-2.1

RUN cd hy3dpaint/custom_rasterizer && \
    pip install --no-build-isolation -e .

RUN cd hy3dpaint/DifferentiableRenderer && \
    bash compile_mesh_painter.sh

RUN mkdir -p hy3dpaint/ckpt && \
    wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth \
    -P hy3dpaint/ckpt

EXPOSE 8081

CMD ["python","api_server.py"]
