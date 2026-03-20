#!/bin/bash

# Check if venv exists, create it if not
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "Virtual environment found."
fi

# Activate
echo "Activating virtual environment..."
source ./venv/bin/activate

echo "Done! You are now in the venv."