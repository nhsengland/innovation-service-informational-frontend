#!/bin/sh

# Wait until all dependencies are met (PostGreSQL)
/wait

# Run migrations
python3 manage.py migrate

# Update search index
python3 manage.py update_index

# Run server
exec gunicorn \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers "${GUNICORN_WORKERS:-1}" \
  --timeout "${GUNICORN_TIMEOUT:-60}" \
  --graceful-timeout "${GUNICORN_GRACEFUL_TIMEOUT:-30}" \
  --access-logfile - \
  --error-logfile - \
  is_homepage.wsgi:application
