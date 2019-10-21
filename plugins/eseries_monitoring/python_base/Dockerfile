ARG TAG=latest
ARG PROJ_NAME=ntap-grafana
FROM ntap-grafana-plugin/eseries_monitoring/alpine-base as builder
# Signifies this is a temporary image that can be purged
LABEL autodelete="true"

FROM python:3.7-alpine3.10
ARG PIP_CONF=pip.conf.internal
ADD $PIP_CONF /etc/pip.conf
COPY --from=builder /etc/apk/repositories /etc/apk/repositories
ONBUILD WORKDIR /home
ONBUILD COPY requirements.txt .
ONBUILD RUN apk update && apk upgrade && rm -rf /var/cache/apk/*