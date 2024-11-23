# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run bash when the container launches
CMD ["/bin/bash"]