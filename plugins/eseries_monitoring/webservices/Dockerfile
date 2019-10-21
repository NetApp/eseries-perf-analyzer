ARG TAG=latest
ARG PROJ_NAME=ntap-grafana
FROM netapp/eseries-webservices:3.20 as base
ADD wsconfig.xml ./wsconfig.xml
LABEL autodelete="true"
FROM plugin/eseries_monitoring/alpine-base
WORKDIR /opt/netapp/webservices_proxy
RUN apk add openjdk8-jre
COPY --from=base /opt/netapp/webservices_proxy ./
CMD ["./webserver.sh"]