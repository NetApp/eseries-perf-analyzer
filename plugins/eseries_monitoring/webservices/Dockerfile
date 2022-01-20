ARG CONTAINER_WEBSERVICES_TAG=5.10
ARG TAG=latest
ARG PROJ_NAME=ntap-grafana
FROM netapp/eseries-webservices:${CONTAINER_WEBSERVICES_TAG} as base
ADD wsconfig.xml ./wsconfig.xml
LABEL autodelete="true"

FROM ${PROJ_NAME}-plugin/eseries_monitoring/alpine-base
WORKDIR /opt/netapp/webservices_proxy
RUN apk add openjdk8-jre
COPY --from=base /opt/netapp/webservices_proxy ./
COPY users.properties ./data/config/
CMD ["./webserver.sh"]
