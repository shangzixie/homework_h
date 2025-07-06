#!/bin/bash
project_dir=$(dirname $(dirname $(realpath $0)))

# active the venv
source $project_dir/.venv/bin/activate
# install the requirements
pip cache purge
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r $project_dir/webapp/requirements.txt