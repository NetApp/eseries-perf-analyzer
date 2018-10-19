#!/bin/sh
if [[ -z "${USERNAME}" ]] || [[ -z "${PASSWORD}" ]]; then # potential environment vars from Dockerfile
    python collector.py --proxySocketAddress ${PROXY_ADDRESS} --intervalTime ${COLLECTION_INTERVAL} -i -s
else
    python collector.py -u ${USERNAME} -p ${PASSWORD} --proxySocketAddress ${PROXY_ADDRESS} --intervalTime ${COLLECTION_INTERVAL} -i -s
fi
