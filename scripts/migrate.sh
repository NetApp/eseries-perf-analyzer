#!/bin/sh

##
## Configuration
##
HOST_NAME="localhost"
GRAFANA_USER="admin"
GRAFANA_PASS="admin"

# install dependencies
pip install requests
pip install influxdb
rm -rf /root/.cache
# run migration script
python /home/scripts/migrate.py -n ${HOST_NAME} -u ${GRAFANA_USER} -p ${GRAFANA_PASS}
