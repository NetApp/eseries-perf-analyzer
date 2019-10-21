#!/bin/bash

plugins_build_info_files=$(find plugins/ -type f -name "build_info.txt")

plugins_build_data=""
for file in $plugins_build_info_files
do
    plugin_name=$(echo $file | grep -o "/.*/" | cut -d "/" -f 2)
    plugin_dir=$(echo "plugins/${plugin_name}")
    while read -r line
    do
	arr=($line)
	if [ "$plugins_build_data" = "" ]; then
	    plugins_build_data="docker build -t plugin/${plugin_name}/${arr[0]} ${plugin_dir}/${arr[1]}"    
	    else
	        plugins_build_data="$plugins_build_data; docker build -t plugin/${plugin_name}/${arr[0]} ${plugin_dir}/${arr[1]}"
		fi
	
    done < $file
done

echo $plugins_build_data
