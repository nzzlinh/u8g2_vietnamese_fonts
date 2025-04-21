#!/bin/bash
# Check if the script is being run from the correct directory
if [ ! -d "scripts" ]; then
  echo "Please run this script from the root directory of the project."
  exit 1
fi
# Check if the make.py script exists
if [ ! -f "scripts/make.py" ]; then
  echo "make.py script not found in the scripts directory."
  exit 1
fi
# Check if the render.py script exists
if [ ! -f "scripts/render.py" ]; then
  echo "render.py script not found in the scripts directory."
  exit 1
fi  
# Check if the make.py script is executable
if [ ! -x "scripts/make.py" ]; then
  echo "make.py script is not executable. Making it executable..."
  chmod +x scripts/make.py
fi
# Check if the render.py script is executable
if [ ! -x "scripts/render.py" ]; then
  echo "render.py script is not executable. Making it executable..."
  chmod +x scripts/render.py
fi
# Run the make.py script
echo "Running make.py script..."
python3 scripts/make.py
if [ $? -ne 0 ]; then
  echo "make.py script failed."
  exit 1
fi
# Run the render.py script
echo "Running render.py script..."
python3 scripts/render.py
if [ $? -ne 0 ]; then
  echo "render.py script failed."
  exit 1
fi
echo "Both scripts ran successfully."
# Check if the output directory exists
