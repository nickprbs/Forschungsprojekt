#!/bin/bash

# Check if virtual environment already exists
if [ ! -d "venv" ]; then
  # Create virtual environment
  sudo python3 -m venv venv
  echo "Created virtual environment"
else
  echo "Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate

# install requirements
sudo pip install -r requirements.txt

echo "Installed requirements."
