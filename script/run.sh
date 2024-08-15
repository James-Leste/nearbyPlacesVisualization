#!/bin/bash


current_dir=$(pwd)

# Print the current working directory
echo "The current working directory is: $current_dir"

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "requirements.txt not found!"
    exit 1
fi

# Install packages listed in requirements.txt
echo "Installing required packages..."
pip install -r requirements.txt

# Check if the installation was successful
if [ $? -eq 0 ]; then
    echo "Packages installed successfully!"
else
    echo "Failed to install some packages."
    exit 1
fi

if [ ! -f "./script/app.py" ]; then
    echo "app.py not found in the current directory!"
    exit 1
fi

# Execute the Python script
echo "Executing app.py..."
python ./script/app.py
