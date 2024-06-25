# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 1213 available to the world outside this container
EXPOSE 1213

# Define environment variables
ENV MODEL_DIR=/app/models/dz_to_en
ENV TOKENIZER_DIR=/app/models/tokenizer_dz_to_en

# Copy the models and tokenizer into the container
COPY ./model/dz_to_en /app/models/dz_to_en
COPY ./model/tokenizer_dz_to_en /app/models/tokenizer_dz_to_en

# Run uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "1213"]
