#!/bin/sh
python collector.py --proxySocketAddress ${PROXY_ADDRESS} --intervalTime ${COLLECTION_INTERVAL} -i -s
