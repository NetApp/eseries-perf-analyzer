#!/bin/bash

# Build/rebuild any images that can be built
docker-compose build

# Start using our compose file and run in the background
docker-compose up -d

# Build an image that will allow us to run an Ansible playbook
docker build -t ansible ansible

# Start an instance of our Ansible image to perform setup on the running instance
#  We run using the host network so that we can access not only the WSP instance, but also the individual containers.
docker run --network "host" ansible

docker ps