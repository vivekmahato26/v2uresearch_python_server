#!/bin/bash

# Configuration
BRANCH="dev"
VENV_PATH="../v2ur-env"  # Adjust if your virtualenv is elsewhere

echo "=========================================="
echo "Starting Deployment Process..."
echo "=========================================="

# 1. Pull Latest Changes
echo "Pulling latest changes from git ($BRANCH)..."
git pull origin $BRANCH

# 2. Activate Virtual Environment
if [ -d "$VENV_PATH" ]; then
    echo "Activating virtual environment..."
    source $VENV_PATH/bin/activate
else
    echo "WARNING: Virtual environment not found at $VENV_PATH. Running with system python or active env."
fi

# 3. Install Dependencies
echo "Installing/Updating requirements..."
pip install -r requirements.txt

# 4. Apply Migrations
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# 5. Collect Static Files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# 6. Restart Server (Adjust based on your setup)
echo "=========================================="
echo "Deployment tasks complete."
echo "IMPORTANT: You may need to restart your application server."
echo "Examples:"
echo "  sudo systemctl restart gunicorn"
echo "  sudo systemctl restart uwsgi"
echo "  sudo supervisorctl restart all"
echo "=========================================="
