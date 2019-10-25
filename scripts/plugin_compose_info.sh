#!/bin/bash

# find all of the docker-compose files for each plugin
plugins_compose_files=$(find plugins/ -type f -name "docker-compose.yml")

# construct our compose commands
plugins_compose_data=""
for file in $plugins_compose_files
do
    if [ "$plugins_compose_data" = "" ]; then
	plugins_compose_data="docker-compose -f ${file} $1"
    else
	plugins_compose_data="${plugins_compose_data}; docker-compose -f ${file} $1"
    fi
done

# return our final compose commands for all plugins
echo $plugins_compose_data
