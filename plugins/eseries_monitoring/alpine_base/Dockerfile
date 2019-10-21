ARG TAG=latest
FROM alpine:3.10
LABEL VERSION=${TAG}
ARG REPO_FILE=repositories.internal
ADD $REPO_FILE /etc/apk/repositories
ONBUILD RUN apk update && apk upgrade && rm -rf /var/cache/apk/*