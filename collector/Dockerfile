FROM python:3.7.2-alpine3.9
WORKDIR /home

ADD requirements.txt .
ADD config.json .
# Determine if we have a connection to the public internet (flawed, yes), and use an offline mirror repo if not.
RUN (ping -c 1 google.com && pip install --default-timeout=3 -r requirements.txt) || \
  pip install --trusted-host repoproxy-rtp.eng.netapp.com --default-timeout=3 -i http://repoproxy-rtp.eng.netapp.com:8081/artifactory/api/pypi/python-package-index/simple -r requirements.txt

ENV COLLECTION_INTERVAL=30
ENV PROXY_ADDRESS=localhost:8080

ADD *.py ./
ADD docker-entrypoint.sh ./
RUN chmod +x *.sh *.py

ENTRYPOINT ["./docker-entrypoint.sh"]

