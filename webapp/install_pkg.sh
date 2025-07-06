#!/bin/bash
project_dir=$(dirname $(dirname $(realpath $0)))

# Create venv if it doesn't exist
if [ ! -d "$project_dir/.venv" ]; then
    echo "Creating virtual environment at $project_dir/.venv..."
    python3 -m venv $project_dir/.venv
fi
# activate the venv
source $project_dir/.venv/bin/activate
# install the requirements
pip cache purge
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r $project_dir/webapp/requirements.txt