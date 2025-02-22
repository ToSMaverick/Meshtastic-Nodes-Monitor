#!/bin/bash

# Exit the script if any command fails
set -e

# Step 1: Update the repository
if [ -d .git ]; then
    #fixing ownership issue
    git config --global --add safe.directory /app
    
    echo "Updating the repository..."
    git pull
else
    echo "Git repository not found, skipping git pull."
fi

# Step 2: Create a virtual environment and install dependencies
if [ ! -d ".venv" ]; then
    echo "Creating a virtual environment..."
    python -m venv .venv
fi

echo "Activating the virtual environment and installing dependencies..."
source .venv/bin/activate
pip install --no-cache-dir -r requirements.txt

# Step 3: Create the configuration file if it doesn't exist
if [ ! -f config.toml ]; then
    echo "Copying sample-config.toml to config.toml..."
    cp sample-config.toml config.toml
fi

# Step 4: Execute the Python script
echo "Starting main.py..."
python app.py
