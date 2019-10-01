#!/bin/bash

docker run --rm -v $PWD/collector:/home/collector ntap-grafana/python-base:2.0 /bin/sh -c "chmod +x /home/collector/tests/runtests.sh;/home/collector/tests/runtests.sh"
rm -f $PWD/collector/tests/collector.py
rm -rf $PWD/collector/tests/__pycache__
