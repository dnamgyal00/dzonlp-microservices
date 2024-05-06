# Use the official Python image as the base image
FROM python:3.10.0

# Set the working directory inside the container
WORKDIR /app

# Install PyTorch
RUN pip install transformers
RUN pip install flask
RUN pip install torch

# Copy the Python script and model files into the container
COPY model/ ./model/
COPY en_to_dz_nmt.py .

# Expose a port (if needed)
EXPOSE 8000

# Command to run the Python script
CMD ["python", "en_to_dz_nmt.py"]
