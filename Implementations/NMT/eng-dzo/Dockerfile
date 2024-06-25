# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 1212 available to the world outside this container
EXPOSE 1212

# Define environment variables (optional, if you need specific paths)
ENV MODEL_DIR=/app/models/en_to_dz
ENV TOKENIZER_DIR=/app/models/tokenizer_en_to_dz

# Copy the models and tokenizer into the container
COPY ./model/en_to_dz /app/models/en_to_dz
COPY ./model/tokenizer_en_to_dz /app/models/tokenizer_en_to_dz

# Run uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "1212"]
