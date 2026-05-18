# Use an official Python runtime based on Debian 12 "bookworm" as a parent image.
FROM python:3.12-slim-bookworm

# Add user that will be used in the container.
#RUN useradd wagtail

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet \
  && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    postgresql-client \
  && rm -rf /var/lib/apt/lists/*

# Install the application server.
RUN pip install "gunicorn==20.0.4"

## Add the wait script to the image
ENV WAIT_VERSION 2.12.1
ADD --chmod=777 https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait

# Install the project requirements.
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Update wagtail module paths
RUN wagtail updatemodulepaths

# Copy the wagtail script
COPY manage.py /manage.py

# Copy startup script
COPY --chmod=777 ./.scripts/wagtail.sh /startup.sh

# Run server
CMD ["/startup.sh"]