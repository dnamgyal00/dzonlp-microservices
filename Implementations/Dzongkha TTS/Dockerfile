# Use the official Python image as the base image.
FROM python:3.9-slim

# Set a working directory.
WORKDIR /app

# Copy the entire directory into the container.
COPY . .

# Install the required dependencies.
RUN pip install TTS
RUN pip install flask
RUN pip install pathlib

# Expose the API port.
EXPOSE 1213

# Start the Flask API.
CMD ["python", "dzo_tts.py"]