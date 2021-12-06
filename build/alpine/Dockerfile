ARG CONTAINER_ALPINE_TAG=3.14.3
ARG TAG=latest
FROM alpine:${CONTAINER_ALPINE_TAG}
LABEL VERSION=${TAG}
ARG REPO_FILE=repositories
ADD $REPO_FILE /etc/apk/repositories
ONBUILD RUN apk update && apk upgrade && rm -rf /var/cache/apk/*
