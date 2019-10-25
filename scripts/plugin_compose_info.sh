#!/bin/bash

# find all of the docker-compose files for each plugin
plugins_compose_files=$(find plugins/ -type f -name "docker-compose.yml")

# construct our compose commands
plugins_compose_data=""
for file in $plugins_compose_files
do
    # extract this plugin's directory name from the docker-compose path
    plugin_name=$(echo $file | grep -o "/.*/" | cut -d "/" -f 2)

    if [ "$plugins_compose_data" = "" ]; then
        plugins_compose_data="echo \"[PLUGINS] '${plugin_name}'\"; docker-compose -f ${file} $1"
    else
        plugins_compose_data="${plugins_compose_data}; echo \"[PLUGINS] '${plugin_name}'\"; docker-compose -f ${file} $1"
    fi
done

# return our final compose commands for all plugins
echo $plugins_compose_data
