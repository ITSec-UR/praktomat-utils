FROM python:3.12

LABEL maintainer="Maximilian Wittig <maximilian.wittig@ur.de>"

WORKDIR /praktomat-utils

# Install required packages
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Add required scripts
COPY src src
CMD python src/main.py
