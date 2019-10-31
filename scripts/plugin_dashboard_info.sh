#!/bin/bash

# find all of the dashboard folders for plugins
plugins_dashboard_folders=$(find plugins/ -mindepth 2 -maxdepth 2 -type d -name "dashboards")

for folder in $plugins_dashboard_folders
do
    # extract this plugin's directory name from the dashboard path
    plugin_name=$(echo $folder | grep -o "/.*/" | cut -d "/" -f 2)

    # create directory for this plugin's dashboards
    mkdir -p "ansible/dashboards/${plugin_name}"

    # find all dashboards for this plugin and copy them to ansible's import directory
    find_dashboards=("ls ${folder}/*.json")
    for file in $find_dashboards
    do
	if [ "${file}" != "ls" ]; then
	    cp -r "${file}" "ansible/dashboards/${plugin_name}/"
	fi
    done
done
