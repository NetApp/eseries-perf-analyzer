ARG TAG=latest
FROM alpine:3.9
ARG REPO_FILE=repositories
ADD $REPO_FILE /etc/apk/repositories
ONBUILD RUN apk update && apk upgrade && rm -rf /var/cache/apk/*
