#!/bin/bash

set -ex

# find all of the build_info text files for each plugin
# these tell us how to build the images in the plugins
plugins_build_info_files=$(find plugins/ -mindepth 2 -maxdepth 2 -type f -name "build_info.txt")

# construct our remove commands
plugins_remove_data=""
for file in $plugins_build_info_files
do
    # extract this plugin's directory name from the build_info path
    plugin_name=$(echo $file | grep -o "/.*/" | cut -d "/" -f 2)

    # read build_info line by line, constructing remove commands
    # build tag: ntap-grafana-plugin/*plugin_dir*/*plugin_component*
    while read -r line
    do
        # ignore empty lines
        if [ "$line" = "" ]; then
            continue
        fi
        # ignore commented lines
        if [ "$(echo $line | cut -b 1)" = "#" ]; then
            continue
        fi

        arr=($line)

        # the image tag is optional, so if not provided just use the image directory
        image_dir=${arr[0]}
        image_tag=${arr[1]}
        if [ ! $image_tag ]; then
            image_tag=$image_dir
        fi

        if [ "$plugins_remove_data" = "" ]; then
            plugins_remove_data="docker rmi -f ${PROJ_NAME}-plugin/${plugin_name}/${image_tag}"
        else
            plugins_remove_data="$plugins_remove_data; docker rmi -f ${PROJ_NAME}-plugin/${plugin_name}/${image_tag}"
        fi
        
    done < $file
done

# return our final remove commands for all plugins
echo $plugins_remove_data
