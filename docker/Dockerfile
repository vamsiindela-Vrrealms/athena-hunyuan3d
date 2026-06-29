FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

ENV CUDA_HOME=/usr/local/cuda
ENV PATH=$CUDA_HOME/bin:$PATH
ENV LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python-is-python3 \
    git \
    wget \
    curl \
    unzip \
    build-essential \
    blender \
    cmake \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libegl1 \
    libxi6 \
    libxkbcommon-x11-0 \
    python3-dev \
    libeigen3-dev \
    libcgal-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python --version
RUN pip --version
RUN nvcc --version

WORKDIR /workspace

COPY . .

RUN pip install --upgrade pip setuptools wheel

RUN pip install \
    torch==2.5.1 \
    torchvision==0.20.1 \
    torchaudio==2.5.1 \
    --index-url https://download.pytorch.org/whl/cu124

# Remove torch packages from requirements
RUN grep -v "^torch==" requirements-working.txt | \
    grep -v "^torchvision==" | \
    grep -v "^torchaudio==" > /tmp/requirements.txt

# Install remaining packages
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN cd hy3dpaint/custom_rasterizer && \
    pip install --no-build-isolation -e .

RUN cd hy3dpaint/DifferentiableRenderer && \
    bash compile_mesh_painter.sh

RUN mkdir -p hy3dpaint/ckpt && \
    wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth \
    -O hy3dpaint/ckpt/RealESRGAN_x4plus.pth

EXPOSE 8081

CMD ["python","api_server.py"]
