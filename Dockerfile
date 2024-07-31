# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install git
RUN apt-get update && apt-get install -y git && apt-get clean

# Create a directory for the app
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . /app/

# Download Whisper model
RUN python -c "import whisper; model = whisper.load_model('base')"

# Expose the port the app runs on
EXPOSE 5000

# Command to run the app
CMD ["python", "server.py"]