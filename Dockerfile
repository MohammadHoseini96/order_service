# Pull base image
FROM python:3.10.2-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN  apt-get update
RUN apt-get install -y --no-install-recommends build-essential libxmlsec1 libxmlsec1-dev libpq-dev postgresql-client python3-dev postgresql-contrib
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

# Install dependencies
#RUN
COPY ./requirements.txt .
COPY ./requirements .
COPY ./requirements/* ./requirements/
RUN pip install -r requirements.txt

# Copy project
COPY . .