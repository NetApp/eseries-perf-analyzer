FROM python:3.7-alpine3.9
WORKDIR /home
# Determine if we have a connection to the public internet (flawed, yes), and use an offline mirror repo if not.
RUN (ping -c 1 google.com && apk --update add ansible) || \
(echo 'http://repomirror-ict.eng.netapp.com/alpine-linux/v3.9/main' > /etc/apk/repositories && apk --update add ansible)
ADD tasks /home/tasks
ADD main.yml /home/
ADD backup.yml /home/
ADD datastore.json /home/
ADD arrays /home/arrays
ADD dashboards /home/dashboards
RUN mkdir -p /etc/ansible && touch /etc/ansible/hosts && mkdir -p /home/dashboards/backup
ENTRYPOINT ["ansible-playbook", "-v"]
CMD ["main.yml"]
