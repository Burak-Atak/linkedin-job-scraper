#!/bin/bash

python3.9 -m venv venv

# activate the virtual environment
source venv/bin/activate
# Install dependencies
echo "Installing dependencies"
pip install -r requirements.txt

# Collect static files
echo "Collecting static files"
python3 manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations"
python3 manage.py migrate
