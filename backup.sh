#!/bin/bash

docker run --rm --name tempbak --network "host" -v `pwd`/ansible/dashboards/backup:/home/dashboards/backup ansible backup.yml
echo -e "******* [ Dashboards backup made in the \"./ansible/dashboards/backup/\" directory ] *******\n"
