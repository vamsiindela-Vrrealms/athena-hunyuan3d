FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# -------------------------------------------------------
# System packages
# -------------------------------------------------------
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
    libcgal-dev \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------------------------------
# Install Miniconda
# -------------------------------------------------------
RUN wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh

ENV PATH=/opt/conda/bin:$PATH

RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main && \
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

RUN conda create -y -n athena python=3.10

SHELL ["/bin/bash", "-c"]

# -------------------------------------------------------
# Python environment
# -------------------------------------------------------
RUN source /opt/conda/bin/activate athena && \
    pip install --upgrade pip setuptools wheel ninja

RUN source /opt/conda/bin/activate athena && \
    pip install --no-cache-dir \
        torch==2.5.1 \
        torchvision==0.20.1 \
        torchaudio==2.5.1 \
        --index-url https://download.pytorch.org/whl/cu124

# -------------------------------------------------------
# Copy repository
# -------------------------------------------------------
WORKDIR /workspace

COPY requirements-working.txt /tmp/requirements.txt

RUN sed -i '/^bpy==/d' /tmp/requirements.txt

RUN source /opt/conda/bin/activate athena && \
    pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /workspace/Hunyuan3D-2.1

WORKDIR /workspace/Hunyuan3D-2.1

# -------------------------------------------------------
# Install project requirements
# -------------------------------------------------------

# -------------------------------------------------------
# Build rasterizer
# -------------------------------------------------------
RUN source /opt/conda/bin/activate athena && \
    cd hy3dpaint/custom_rasterizer && \
    pip install --no-build-isolation -e .

# -------------------------------------------------------
# Build renderer
# -------------------------------------------------------
RUN source /opt/conda/bin/activate athena && \
    cd hy3dpaint/DifferentiableRenderer && \
    bash compile_mesh_painter.sh

# -------------------------------------------------------
# Download ESRGAN checkpoint
# -------------------------------------------------------
RUN mkdir -p hy3dpaint/ckpt && \
    wget -q \
    https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth \
    -O hy3dpaint/ckpt/RealESRGAN_x4plus.pth

# -------------------------------------------------------
# Runtime
# -------------------------------------------------------
ENV PATH=/opt/conda/envs/athena/bin:$PATH

EXPOSE 8081

CMD ["python","api_server.py"]
