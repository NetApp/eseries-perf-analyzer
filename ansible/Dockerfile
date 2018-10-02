FROM python:2.7
WORKDIR /home
RUN pip install --default-timeout=3 ansible ||\
  pip install --trusted-host repoproxy-rtp.eng.netapp.com --default-timeout=3 -i http://repoproxy-rtp.eng.netapp.com:8081/artifactory/api/pypi/python-package-index/simple ansible
ADD tasks /home/tasks
ADD main.yml /home/
ADD backup.yml /home/
ADD datastore.json /home/
ADD arrays /home/arrays
ADD dashboards /home/dashboards
RUN mkdir -p /etc/ansible && touch /etc/ansible/hosts
ENTRYPOINT ["ansible-playbook", "-v"]
CMD ["main.yml"]