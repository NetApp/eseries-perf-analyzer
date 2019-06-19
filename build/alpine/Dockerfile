ARG TAG=latest
FROM alpine:3.9
LABEL VERSION=${TAG}
ARG REPO_FILE=repositories
ADD $REPO_FILE /etc/apk/repositories
ONBUILD RUN apk update && apk upgrade && rm -rf /var/cache/apk/*
