# Use Ubuntu as the base image
FROM ubuntu:20.04

# Update package lists and install necessary packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        openjdk-8-jre-headless \
        software-properties-common \
        gnupg \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys EEA14886 \
    && add-apt-repository ppa:openjdk-r/ppa \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        openjdk-8-jre-headless \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
RUN pip install flask flask-cors pydub TTS

# Copy the TTS application files into the container
COPY tts /app

# Run the application
CMD ["python3", "dzo_tts.py"]
