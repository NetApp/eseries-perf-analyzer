#!/bin/bash

docker run --network "host" ansible backup.yml
id=$(docker create ansible)
docker cp $id:/home/dashboards ./ansible/dashboards/backup
docker rm -v $id
