#!/bin/sh
python collector.py --username ${USERNAME} --password ${PASSWORD} --proxySocketAddress ${PROXY_ADDRESS} --intervalTime ${COLLECTION_INTERVAL} -i -s
