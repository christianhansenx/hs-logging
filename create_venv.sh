#!/bin/bash

deactivate
rm -rf .venv
pip install --upgrade setuptools pip
pip install virtualenv
virtualenv -p python3 .venv

source .venv/bin/activate
