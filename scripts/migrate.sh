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
# install dependencies
pip install requests
pip install influxdb
rm -rf /root/.cache
# run migration script
python /home/scripts/migrate.py -n ${HOST_NAME} -u ${GRAFANA_USERNAME} -p ${GRAFANA_PASSWORD} -w ${PROXY_USERNAME} -a ${PROXY_PASSWORD}
