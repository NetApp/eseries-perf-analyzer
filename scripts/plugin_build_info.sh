#!/bin/bash

# find all of the build_info text files for each plugin
# these tell us how to build the plugins
plugins_build_info_files=$(find plugins/ -type f -name "build_info.txt")

# prepend message signifying we're beginning plugin build phase
plugins_build_data="echo \"[PLUGINS] Beginning plugins build...\""

# construct our build commands
for file in $plugins_build_info_files
do
    # extract this plugin's directory name from the build_info path
    plugin_name=$(echo $file | grep -o "/.*/" | cut -d "/" -f 2)

    # relative path to this plugin's directory
    plugin_dir=$(echo "plugins/${plugin_name}")

    # append a message signaling we're beginning to build this plugin
    plugins_build_data="$plugins_build_data; echo \"[PLUGINS] Building plugin: ${plugin_name}\""

    # read this plugin's build_info line by line, constructing build commands for its components
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
        if [ "$plugins_build_data" = "" ]; then
            plugins_build_data="echo \"[PLUGINS] Building '${plugin_name}' component: ${arr[0]}\"; docker build --build-arg PROJ_NAME=${PROJ_NAME} -t ${PROJ_NAME}-plugin/${plugin_name}/${arr[0]} ${plugin_dir}/${arr[1]}"    
        else
            plugins_build_data="$plugins_build_data; echo \"[PLUGINS] Building '${plugin_name}' component: ${arr[0]}\"; docker build --build-arg PROJ_NAME=${PROJ_NAME} -t ${PROJ_NAME}-plugin/${plugin_name}/${arr[0]} ${plugin_dir}/${arr[1]}"
        fi
        
    done < $file
done

# return our final build command
# this contains display output for which plugins are building, and the corresponding docker build commands
echo $plugins_build_data
