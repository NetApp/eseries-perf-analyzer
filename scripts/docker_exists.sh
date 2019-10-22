#!/bin/bash

if command -v docker &>/dev/null; then
    if command -v docker-compose &>/dev/null; then
        exit 0
    else
        echo "#########################################################################################################"
        echo "! Unable to find Docker Compose, is it installed?                                                       !"
        echo "! This application makes extensive use of Docker Compose. Check our documentation for more information. !"
        echo "#########################################################################################################"
        exit 1
    fi
else
    echo "#################################################################################################"
    echo "! Unable to find Docker, is it installed?                                                       !"
    echo "! This application makes extensive use of Docker. Check our documentation for more information. !"
    echo "#################################################################################################"
    exit 1
fi
