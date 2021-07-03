ARG TAG=latest
FROM alpine:3.12
LABEL VERSION=${TAG}
ARG ALPINE_REPO_FILE=repositories
ADD $ALPINE_REPO_FILE /etc/apk/repositories
ONBUILD RUN apk update && apk upgrade && rm -rf /var/cache/apk/*