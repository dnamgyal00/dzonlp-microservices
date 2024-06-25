# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . .

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Make port 1215 available to the world outside this container
EXPOSE 1215

# Define environment variables
ENV MODEL_DIR=/app/models/

# Copy the models into the container
COPY ./model/ /app/models/

# Run Flask server
CMD ["python", "main.py"]
