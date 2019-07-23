ARG TAG=latest
FROM ntap-grafana/python-base:${TAG}
ENV COLLECTION_INTERVAL=30
ENV PROXY_ADDRESS=webservices:8080
RUN pip install --trusted-host repoproxy-rtp.eng.netapp.com -i http://repoproxy-rtp.eng.netapp.com:8081/artifactory/api/pypi/python-package-index/simple -r requirements.txt && rm -rf /root/.cache

ADD docker-entrypoint.sh config.json *.py ./
RUN chmod +x *.sh *.py

ENTRYPOINT ["./docker-entrypoint.sh"]
