#!/bin/bash

docker run --rm -v $PWD/collector:/home/collector $1/python-base:$2 /bin/sh -c "chmod +x /home/collector/tests/runtests.sh;/home/collector/tests/runtests.sh"
