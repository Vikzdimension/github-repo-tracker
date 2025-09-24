#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Build React frontend
cd backend/frontend/admin-dashboard
npm install
npm run build
cd ../../../

# Collect static files
cd backend
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate