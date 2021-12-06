ARG CONTAINER_ALPINE_TAG=3.14.3
ARG TAG=latest
FROM alpine:${CONTAINER_ALPINE_TAG}
LABEL VERSION=${TAG}
ARG ALPINE_REPO_FILE=repositories
ADD $ALPINE_REPO_FILE /etc/apk/repositories
ONBUILD RUN apk update && apk upgrade && rm -rf /var/cache/apk/*
