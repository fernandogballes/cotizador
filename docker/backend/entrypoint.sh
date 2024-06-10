#!/bin/bash
# docker/backend/entrypoint.sh

# Apply database migrations
python Sistema/backend/manage.py makemigrations
python Sistema/backend/manage.py migrate

# Start the Django server
exec "$@"
