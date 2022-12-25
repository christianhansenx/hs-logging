#!/bin/bash

python3 -m pip install --upgrade -r requirements_wsl_ubuntu.txt

mkdir -p workspace/testing
python3 -m pip freeze --all 2>&1 | tee workspace/testing/pip_list_dev_$(date +"%FT%H%M%S%z").txt
