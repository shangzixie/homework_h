#!/bin/bash
project_dir=$(dirname $(dirname $(realpath $0)))

# active the venv
source $project_dir/.venv/bin/activate
# run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000