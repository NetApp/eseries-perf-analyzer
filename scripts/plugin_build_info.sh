#!/bin/bash

set -ex

# grab our environment variables
# and construct our build args string
env_vars=$(cat .env)
env_var_names=($(cat .env | cut -d "=" -f 1))
env_var_values=($(cat .env | cut -d "=" -f 2))
env_var_string=""
index=0
for s in $env_vars
do
    this_name=${env_var_names[index]}
    this_value=${env_var_values[index]}
    if [ "$env_var_string" = "" ]; then
	env_var_string="--build-arg $this_name=$this_value "
    else
	env_var_string="--build-arg $this_name=$this_value $env_var_string"
    fi
    index=$index+1
done

# find all of the build_info text files for each plugin
# these tell us how to build the plugins
plugins_build_info_files=$(find plugins/ -mindepth 2 -maxdepth 2 -type f -name "build_info.txt")

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

        # the image tag is optional, so if not provided just use the image directory
        image_dir=${arr[0]}
        image_tag=${arr[1]}
        if [ ! $image_tag ]; then
            image_tag=$image_dir
        fi

        # add this component to the build commands
        if [ "$plugins_build_data" = "" ]; then
            plugins_build_data="echo \"[PLUGINS] Building '${plugin_name}' component: ${image_tag}\"; docker build --build-arg PROJ_NAME=${PROJ_NAME} $env_var_string -t ${PROJ_NAME}-plugin/${plugin_name}/${image_tag} ${plugin_dir}/${image_dir}"
        else
            plugins_build_data="$plugins_build_data; echo \"[PLUGINS] Building '${plugin_name}' component: ${image_tag}\"; docker build --build-arg PROJ_NAME=${PROJ_NAME} $env_var_string -t ${PROJ_NAME}-plugin/${plugin_name}/${image_tag} ${plugin_dir}/${image_dir}"
        fi
        
    done < $file
done

# return our final build command
# this contains display output for which plugins are building, and the corresponding docker build commands
echo $plugins_build_data
