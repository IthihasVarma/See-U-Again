# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Health check to ensure the app is running
HEALTHCHECK CMD curl --fail http://localhost:5006/ || exit 1

# Command to run the application
CMD ["python", "app.py"]
