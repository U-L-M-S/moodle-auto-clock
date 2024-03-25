# Use an official Python runtime as a parent image
FROM python:3.9

# Install Chrome and Chromedriver
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
 && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
 && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
 && apt-get update \
 && apt-get install -y google-chrome-stable 

# Set up working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# It can be 'starten' or 'beenden'
ENV ACTION=

# Run the Python script
CMD ["python", "main.py"]
