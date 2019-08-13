#!/bin/sh

##
# Configuration
##
HOST_NAME="localhost"
PROXY_USERNAME="admin"
PROXY_PASSWORD="admin"
GRAFANA_USERNAME="admin"
GRAFANA_PASSWORD="admin"

##
# Execution
##
# create a virtual environment for python
python -m venv ./env
source ./env/bin/activate
# install dependencies
pip install -r /home/scripts/requirements.txt --default-timeout=5 --retries 15
# run migration script
exec python /home/scripts/migrate.py -n ${HOST_NAME} -u ${GRAFANA_USERNAME} -p ${GRAFANA_PASSWORD} -w ${PROXY_USERNAME} -a ${PROXY_PASSWORD}
