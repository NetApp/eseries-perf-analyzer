#!/bin/bash

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -q|--quiet)
    QUIET="yes"
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}"

# If they haven't passed the --quiet argument.
if [ -z "$QUIET" ]; then
    echo "##########################################################################################"
    echo "In order to run this application the following Docker images will be downloaded and installed:"
    find . -iname "Dockerfile" -exec cat {} \; | grep ^FROM | awk '{print $2}' | grep -v "^\\$" | sort -u
    echo ''
    echo "If you agree with the above you may continue, otherwise cancel and
  change the relevant tags to a newer version in the Dockerfile[s]."
    echo "Be aware that the images configured in the repository
  are the tested images and we cannot guarantee correct
  behavior if you update the images to a new tag."
    read -rp "Would you like to continue? [y/n] "
else
    REPLY=yes
fi

if [[ ${REPLY,,} =~ ^(y|yes|Yes|YES)$ ]]; then
   exit 0
else
    echo ''
    echo "You have elected to not continue."
    echo "Update the Docker images in the relevant files and then re-run this script:"
    find . -iname "Dockerfile" -exec echo {} \;
    exit 1
fi
