#!/bin/bash

# Check if venv exists and create if not
if [ ! -d "venv" ]; then
  python3 -m venv venv
  echo "Created virtual environment 'venv'"
fi

# Activate the virtual environment
source venv/bin/activate

# Check if requirements.txt exists and install requirements
if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
  echo "Installed requirements from requirements.txt"
else
  echo "requirements.txt not found.  Please create it or install packages manually."
fi
