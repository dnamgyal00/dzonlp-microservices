# Use the official Python image as the base image.
FROM python:3.11

# Set a working directory.
WORKDIR /app

# copy all files to workdir
COPY . .

# Install the required dependencies.
RUN pip install flask
RUN pip install transformers==4.33.3
RUN pip install torch

# Expose the Flask app port.
EXPOSE 1212

# Start the Flask app.
CMD ["python", "en_to_dz_nmt.py"]
