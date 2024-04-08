# Wait until all dependencies are met (PostGreSQL)
#/wait

# Perform first installation
if [ ! -f tmp/wagtail/installed ]; then
  echo "Finishing Wagtail installation"

  # Run migrations
  python3 manage.py migrate

  # Import Database

  # Import assets

  # Update search index
  python3 manage.py update_index
  
  touch /tmp/installed
fi

python3 manage.py runserver 0.0.0.0:8000
