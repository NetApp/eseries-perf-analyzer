#!/bin/bash

# find all of the task folders for plugins
plugins_task_folders=$(find plugins/ -maxdepth 2 -type d -name "ansible_tasks")

for folder in $plugins_task_folders
do
    # extract this plugin's directory name from the task path
    plugin_name=$(echo $folder | grep -o "/.*/" | cut -d "/" -f 2)

    # create directory for this plugin's tasks
    mkdir -p "ansible/tasks/plugin_tasks/${plugin_name}"

    # find all tasks for this plugin and copy them to ansible's task directory
    find_tasks=("ls ${folder}/*.yml")
    for file in $find_tasks
    do
	if [ "${file}" != "ls" ]; then
	    cp -r "${file}" "ansible/tasks/plugin_tasks/${plugin_name}/"
	fi
    done
done
