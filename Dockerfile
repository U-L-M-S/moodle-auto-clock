FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir requests beautifulsoup4

ENV ACTION=""
CMD ["python3", "main.py"]

