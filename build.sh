#!/bin/bash

# Exit on error
set -e

# Step 1: Check if virtual environment exists, if not, create it
if [ ! -d "venv" ]; then
  echo "Virtual environment not found, creating a new one..."
  python3 -m venv venv
else
  echo "Virtual environment found."
fi

# Step 2: Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Step 3: Upgrade pip to the latest version
echo "Upgrading pip..."
pip install --upgrade pip

# Step 4: Install dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Step 5: Run migrations (if applicable)
echo "Running database migrations..."
python manage.py migrate

# Step 6: Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Step 7: Start the Django development server
echo "Starting Django development server..."
python manage.py runserver

# Alternatively, if you need production setup, uncomment this:
# gunicorn myproject.wsgi:application --bind 0.0.0.0:8000
