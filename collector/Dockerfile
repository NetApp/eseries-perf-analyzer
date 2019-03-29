FROM python:3.7-alpine3.9
WORKDIR /home
ENV COLLECTION_INTERVAL=30
ENV PROXY_ADDRESS=localhost:8080

ADD requirements.txt .

# Determine if we have a connection to the public internet (flawed, yes), and use an offline mirror repo if not.
RUN (ping -c 1 google.com && pip install --default-timeout=3 -r requirements.txt) || \
  pip install --trusted-host repoproxy-rtp.eng.netapp.com --default-timeout=3 -i http://repoproxy-rtp.eng.netapp.com:8081/artifactory/api/pypi/python-package-index/simple -r requirements.txt

ADD docker-entrypoint.sh config.json *.py ./
RUN chmod +x *.sh *.py

ENTRYPOINT ["./docker-entrypoint.sh"]
