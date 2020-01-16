#!/bin/bash

# find all of the build_info text files for each plugin
# these tell us how to build the plugins
plugins_build_info_files=$(find plugins/ -mindepth 2 -maxdepth 2 -type f -name "build_info.txt")

# prepend message signifying we're beginning plugin build phase
plugins_save_data=""

# construct our save commands
for file in $plugins_build_info_files
do
    # extract this plugin's directory name from the build_info path
    plugin_name=$(echo $file | grep -o "/.*/" | cut -d "/" -f 2)

    # relative path to this plugin's directory
    plugin_dir=$(echo "plugins/${plugin_name}")

    # read this plugin's build_info line by line, constructing save commands for its components
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

        # add this component to the build commands
        if [ "$plugins_save_data" = "" ]; then
            plugins_save_data="docker save ${PROJ_NAME}-plugin/${plugin_name}/${image_tag} > images/${PROJ_NAME}-plugin-${plugin_name}-${image_tag}.tar"
        else
            plugins_save_data="$plugins_save_data; docker save ${PROJ_NAME}-plugin/${plugin_name}/${image_tag} > images/${PROJ_NAME}-plugin-${plugin_name}-${image_tag}.tar"
        fi
        
    done < $file
done

# return our final build command
# this contains display output for which plugins are building, and the corresponding docker build commands
echo $plugins_save_data
