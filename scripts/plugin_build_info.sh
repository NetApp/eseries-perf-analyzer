#!/bin/bash

# find all of the build_info text files for each plugin
# these tell us how to build the plugins
plugins_build_info_files=$(find plugins/ -type f -name "build_info.txt")

# construct our build commands
plugins_build_data=""
for file in $plugins_build_info_files
do
    # extract this plugin's directory name from the build_info path
    plugin_name=$(echo $file | grep -o "/.*/" | cut -d "/" -f 2)

    # relative path to this plugin's directory
    plugin_dir=$(echo "plugins/${plugin_name}")

    # read build_info line by line, constructing build commands
    # build tag: ntap-grafana-plugin/*plugin_dir*/*plugin_component*
    while read -r line
    do
	arr=($line)
	if [ "$plugins_build_data" = "" ]; then
	    plugins_build_data="docker build -t plugin/${plugin_name}/${arr[0]} ${plugin_dir}/${arr[1]}"    
	    plugins_build_data="docker build -t ${PROJ_NAME}-plugin/${plugin_name}/${arr[0]} ${plugin_dir}/${arr[1]}"    
	    else
	        plugins_build_data="$plugins_build_data; docker build -t plugin/${plugin_name}/${arr[0]} ${plugin_dir}/${arr[1]}"
		    plugins_build_data="$plugins_build_data; docker build -t ${PROJ_NAME}-plugin/${plugin_name}/${arr[0]} ${plugin_dir}/${arr[1]}"
		    fi
	
    done < $file
done

# return our final build command for all plugins
echo $plugins_build_data
