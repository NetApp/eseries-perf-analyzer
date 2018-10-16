#!/bin/bash

docker run --network "host" --rm ansible backup.yml
id=$(docker create ansible)
docker cp $id:/home/dashboards ./ansible/dashboards/backup
