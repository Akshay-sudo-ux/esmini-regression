FROM ubuntu:22.04

# Install basic dependencies
RUN apt-get update && apt-get install -y \
    wget unzip python3 python3-pip \
    libopenscenegraph-dev libglm-dev

# Download and extract ESmini prebuilt binary
WORKDIR /opt
RUN wget https://github.com/esmini/esmini/releases/download/v2.50.4/esmini-bin_Linux.zip && \
    unzip esmini-bin_Linux.zip -d esmini && \
    rm esmini-bin_Linux.zip

# Copy your regression framework into the image
WORKDIR /workspace
COPY . /workspace

# Set environment variable pointing to ESmini executable
ENV ESMINI_BIN=/opt/esmini/esmini/bin/esmini

# Set working directory as default and run the regression script
ENTRYPOINT ["python3", "regression.py"]

