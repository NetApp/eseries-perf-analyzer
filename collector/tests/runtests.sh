#!/bin/sh

##
# Execution
##
# create a virtual environment for python
python -m venv ./env
source ./env/bin/activate
# install dependencies
pip install -r /home/collector/tests/requirements.txt --default-timeout=5 --retries 15
cp /home/collector/tests/*.py /home/collector
# run tests
cd /home/collector
exec python -m unittest
