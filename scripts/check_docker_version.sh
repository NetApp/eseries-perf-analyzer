#!/bin/bash

docker_version=$(docker -v | cut -f 3- -d ' ' | cut -d',' -f1)

IFS='.'
read -ra arr <<< "$docker_version"
if [ ${arr[0]} -lt "17" ]; then
    echo "ERROR: Your Docker version ($docker_version) is too old, you must have at least version 17.05 to make use of this project."
    exit 1
else
    if [ ${arr[0]} = "17" ]; then
	if [ ${arr[1]} -lt "05" ]; then
	    echo "ERROR: Your Docker version ($docker_version) is too old, you must have at least version 17.05 to make use of this project."
	    exit 1
	fi
    fi
fi

IFS=' '
