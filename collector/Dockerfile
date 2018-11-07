FROM python:alpine3.7
WORKDIR /home

ADD requirements.txt .
ADD config.json .

RUN pip install --default-timeout=3 -r requirements.txt ||\
  pip install --trusted-host repoproxy-rtp.eng.netapp.com --default-timeout=3 -i http://repoproxy-rtp.eng.netapp.com:8081/artifactory/api/pypi/python-package-index/simple -r requirements.txt

ENV COLLECTION_INTERVAL=30
ENV PROXY_ADDRESS=localhost:8080

ADD *.py ./
ADD docker-entrypoint.sh ./
RUN chmod +x *.sh *.py
run which sh

ENTRYPOINT ["./docker-entrypoint.sh"]

