FROM python:3.13-slim

LABEL maintainer="Maximilian Wittig <maximilian.wittig@ur.de>"

RUN apt-get update && \
    apt-get install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /praktomat-utils

# Install required packages
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Add required scripts
COPY src src
CMD ["python", "src/main.py"]
