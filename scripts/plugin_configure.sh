#!/bin/bash

# Run any pre-build plugin configuration
echo "Plugin Configuration"

# Configure the webservices proxy password
USERS_TEMPLATE=plugins/eseries_monitoring/webservices/users.template
ROLES=,security.admin,storage.admin,storage.monitor,support.admin
USERS_FILE=plugins/eseries_monitoring/webservices/users.properties

# Include the authentication source file which contains the PROXY_PASSWORD variable
. .auth.env

if [ -z "$PROXY_PASSWORD" ]
then
    echo "PROXY_PASSWORD is not set in .auth.env"
    exit 1
fi

sed "s/^admin=.*/admin=${PROXY_PASSWORD}${ROLES}/" ${USERS_TEMPLATE} > ${USERS_FILE}
