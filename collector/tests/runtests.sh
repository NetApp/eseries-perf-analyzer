#!/bin/sh

##
# Execution
##
# create a virtual environment for python
python -m venv ./env
source ./env/bin/activate
# install dependencies
cd /home/collector/tests
pip install -r requirements.txt --default-timeout=5 --retries 15
cp ../collector.py ./
# run tests
exec python -m unittest
