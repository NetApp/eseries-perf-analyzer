ARG CONTAINER_PYTHON_TAG=3.10-alpine3.14
ARG TAG=latest
ARG PROJ_NAME=ntap-grafana
FROM ${PROJ_NAME}-plugin/eseries_monitoring/alpine-base as builder
# Signifies this is a temporary image that can be purged
LABEL autodelete="true"

FROM python:${CONTAINER_PYTHON_TAG}
ARG PIP_CONF=pip.conf
ADD $PIP_CONF /etc/pip.conf
COPY --from=builder /etc/apk/repositories /etc/apk/repositories
ONBUILD WORKDIR /home
ONBUILD COPY requirements.txt .
ONBUILD RUN apk update && apk upgrade && rm -rf /var/cache/apk/*
