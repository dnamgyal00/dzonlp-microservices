# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Install Java 22 (runtime only, no need for JDK since compilation isn't required)
RUN curl -LO https://download.oracle.com/java/22/latest/jdk-22_linux-x64_bin.tar.gz \
    && mkdir -p /usr/local/java \
    && tar -xzf jdk-22_linux-x64_bin.tar.gz -C /usr/local/java \
    && rm jdk-22_linux-x64_bin.tar.gz \
    && mv /usr/local/java/jdk-22* /usr/local/java/jdk-22

ENV JAVA_HOME=/usr/local/java/jdk-22
ENV PATH="$JAVA_HOME/bin:$PATH"

# Install Rust for building Rust-based projects
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:$PATH"

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Copy the current directory contents into the container at /app
COPY . .

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Make port 1214 available to the world outside this container
EXPOSE 1214

# Run FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "1214"]
