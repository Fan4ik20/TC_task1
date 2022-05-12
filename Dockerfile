# syntax=docker/dockerfile:1
# Author Mark Zaianchkovskyi

FROM python:3.10-slim-buster

WORKDIR /app

# This file contains all software dependencies.
COPY requirements.txt requirements.txt

# Runs installing dependencies from file.
RUN python -m pip install -r requirements.txt

COPY ./server/. .

CMD ["python3", "-u", "app.py"]

