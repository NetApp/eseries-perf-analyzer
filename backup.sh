#!/bin/bash

#rm -rf ./ansible/dashboards/backup
docker run --name tempbak --network "host" ansible backup.yml
docker cp tempbak:/home/dashboards/backup ./ansible/dashboards
docker rm tempbak > /dev/null # suppress output
echo -e "******* [ Dashboards backup made in /ansible/dashboards/backup/ ] *******\n"
