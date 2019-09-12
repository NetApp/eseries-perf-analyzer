#!/bin/sh

# Username and password may be provided via Docker compose file located
# in the root of the project (docker-compose.yml) under stats_collector

if [[ -z "${USERNAME}" ]] || [[ -z "${PASSWORD}" ]]; then
    python collector.py --proxySocketAddress ${PROXY_ADDRESS} --intervalTime ${COLLECTION_INTERVAL} --retention ${RETENTION_PERIOD} -i -s
else
    python collector.py -u ${USERNAME} -p ${PASSWORD} --proxySocketAddress ${PROXY_ADDRESS} --intervalTime ${COLLECTION_INTERVAL} --retention ${RETENTION_PERIOD} -i -s
fi
