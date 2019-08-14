ARG TAG=latest
ARG PROJ_NAME=ntap-grafana
FROM ${PROJ_NAME}/alpine-base:${TAG} as builder
LABEL autodelete="true"

FROM influxdb:1.7-alpine
ADD influxdb.conf /etc/influxdb
COPY --from=builder /etc/apk/repositories /etc/apk/repositories
RUN apk update && apk upgrade && rm -rf /var/cache/apk/*

CMD ["influxd"]
