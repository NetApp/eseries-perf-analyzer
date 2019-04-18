ARG TAG=latest
FROM ntap-grafana/alpine-base:${TAG} as builder
FROM python:3.7-alpine3.9
ARG PIP_CONF=pip.conf
ADD $PIP_CONF /etc/pip.conf
COPY --from=builder /etc/apk/repositories /etc/apk/repositories
ONBUILD WORKDIR /home
ONBUILD COPY requirements.txt .
