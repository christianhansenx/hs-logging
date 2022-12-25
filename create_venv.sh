#!/bin/bash

deactivate
mkdir .venv
sudo pip install virtualenv
virtualenv -p python3 .venv

source .venv/bin/activate
