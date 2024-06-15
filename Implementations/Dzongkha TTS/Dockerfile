# Use the Python 3.10.12 Alpine image as the base
FROM python:3.10.12-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the Python requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application code
COPY dzo_tts.py .

# Expose the port on which the Flask app will run
EXPOSE 1214

# Set the command to run the Flask app
CMD ["python", "dzo_tts.py"]