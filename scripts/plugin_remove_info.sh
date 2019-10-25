#!/bin/bash

# find all of the build_info text files for each plugin
# these tell us how to build the images in the plugins
plugins_build_info_files=$(find plugins/ -type f -name "build_info.txt")

# construct our remove commands
plugins_remove_data=""
for file in $plugins_build_info_files
do
    # extract this plugin's directory name from the build_info path
    plugin_name=$(echo $file | grep -o "/.*/" | cut -d "/" -f 2)

    # relative path to this plugin's directory
    plugin_dir=$(echo "plugins/${plugin_name}")

    # read build_info line by line, constructing remove commands
    # build tag: ntap-grafana-plugin/*plugin_dir*/*plugin_component*
    while read -r line
    do
	arr=($line)
	if [ "$plugins_remove_data" = "" ]; then
	        plugins_remove_data="docker rmi -f ${PROJ_NAME}-plugin/${plugin_name}/${arr[0]}"
		else
	        plugins_remove_data="$plugins_remove_data; docker rmi -f ${PROJ_NAME}-plugin/${plugin_name}/${arr[0]}"
		fi
	
    done < $file
done

# return our final remove commands for all plugins
echo $plugins_remove_data
