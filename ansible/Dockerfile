ARG TAG=latest
ARG PROJ_NAME=ntap-grafana
ARG IMAGE=${PROJ_NAME}/python-base:${TAG}
# Installing Ansible requires gcc and other dependencies to build packages from source. We'll do this in 2 stages so we don't
#   have to have all of the build-time dependencies in the final image.
FROM ${IMAGE} as builder

# Signifies this is a temporary image that can be purged
LABEL autodelete="true"
RUN apk add --update gcc musl-dev libffi-dev make openssl-dev
RUN python -m pip install --upgrade pip
RUN pip --default-timeout=5 --retries 15 install --upgrade --prefix=/install -r requirements.txt

FROM ${IMAGE}
COPY --from=builder /install /usr/local
ADD *.yml *.json ./
ADD dashboards/ ./dashboards
ADD tasks/ ./tasks
RUN mkdir -p /etc/ansible && touch /etc/ansible/hosts && mkdir -p /home/dashboards/backup
ENTRYPOINT ["ansible-playbook", "-v"]
CMD ["main.yml"]
