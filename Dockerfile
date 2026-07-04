FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    git \
    openjdk-11-jdk \
    android-tools-adb \
    curl \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install apktool
RUN wget https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.7.0.jar -O /usr/local/bin/apktool.jar && \
    echo '#!/bin/bash' > /usr/local/bin/apktool && \
    echo 'java -jar /usr/local/bin/apktool.jar "$@"' >> /usr/local/bin/apktool && \
    chmod +x /usr/local/bin/apktool

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot files
COPY . .

# Create necessary directories
RUN mkdir -p /tmp/apk_work /tmp/apk_output

# Set environment
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin

# Run bot
CMD ["python3", "bot.py"]
