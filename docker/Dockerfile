FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
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

WORKDIR /workspace

COPY . .

RUN pip install --upgrade pip setuptools wheel

RUN pip install --no-cache-dir -r requirements-docker.txt

RUN cd hy3dpaint/custom_rasterizer && \
    pip install --no-build-isolation -e .

RUN cd hy3dpaint/DifferentiableRenderer && \
    bash compile_mesh_painter.sh

RUN mkdir -p hy3dpaint/ckpt && \
    wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth \
    -O hy3dpaint/ckpt/RealESRGAN_x4plus.pth

EXPOSE 8081

CMD ["python","api_server.py"]
