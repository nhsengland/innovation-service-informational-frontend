#!/bin/sh

# Wait until all dependencies are met (PostGreSQL)
/wait

# Run migrations
python3 manage.py migrate

# Update search index
python3 manage.py update_index

# Run server
python3 manage.py runserver 0.0.0.0:8000
