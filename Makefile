# import config.
# You can change the default config with `make cnf="config_special.env" build`
cnf ?= .env
include $(cnf)
export $(shell sed 's/=.*//' $(cnf))

configuration ?= ""

TAG ?= 1.0

# external repos
PIP_CONF ?= pip.conf
ALPINE_REPO_FILE ?= repositories


configuration := .$(configuration)

# import deploy config
# You can change the default deploy config with `make dpl="deploy_special.env" release`
dpl ?= deploy.env
include $(dpl)
export $(shell sed 's/=.*//' $(dpl))

# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help warn

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

# DOCKER TASKS
# Build the container
build: warn ## Build the container
	docker build --build-arg REPO_FILE=$(ALPINE_REPO_FILE) --build-arg TAG=$(TAG) -t $(PROJ_NAME)/alpine-base:${TAG} build/alpine
	docker build --build-arg PIP_CONF=$(PIP_CONF) --build-arg TAG=$(TAG) --build-arg PROJ_NAME=$(PROJ_NAME) -t $(PROJ_NAME)/python-base:${TAG} build/python
	docker build --build-arg TAG=$(TAG) --build-arg PROJ_NAME=$(PROJ_NAME) -t $(PROJ_NAME)/ansible:${TAG} ansible
	docker build --build-arg TAG=$(TAG) --build-arg PROJ_NAME=$(PROJ_NAME) -t $(PROJ_NAME)/collector:${TAG} collector
	docker build --build-arg TAG=$(TAG) --build-arg PROJ_NAME=$(PROJ_NAME) -t $(PROJ_NAME)/webservices:$(TAG) webservices
	docker build --build-arg TAG=$(TAG) --build-arg PROJ_NAME=$(PROJ_NAME) -t $(PROJ_NAME)/grafana:$(TAG) grafana
	docker build --build-arg TAG=$(TAG) -t $(PROJ_NAME)/influxdb:$(TAG) influxdb
	docker-compose build

build-nc: warn ## Build the container without caching
	docker build --no-cache -f build/alpine/Dockerfile --build-arg REPO_FILE=$(ALPINE_REPO_FILE) --build-arg TAG=$(TAG) -t $(PROJ_NAME)/alpine-base:${TAG} build/alpine
	docker build --no-cache -f build/python/Dockerfile --build-arg PIP_CONF=$(PIP_CONF) --build-arg TAG=$(TAG) --build-arg PROJ_NAME=$(PROJ_NAME) -t $(PROJ_NAME)/python-base:${TAG} build/python
	docker build --no-cache --build-arg TAG=$(TAG) --build-arg PROJ_NAME=$(PROJ_NAME) -t $(PROJ_NAME)/ansible:${TAG} ansible
	docker build --no-cache --build-arg TAG=$(TAG) --build-arg PROJ_NAME=$(PROJ_NAME) -t $(PROJ_NAME)/collector:${TAG} collector
	docker build --no-cache --build-arg TAG=$(TAG) --build-arg PROJ_NAME=$(PROJ_NAME) -t $(PROJ_NAME)/webservices:$(TAG) webservices
	docker build --no-cache --build-arg TAG=$(TAG) --build-arg PROJ_NAME=$(PROJ_NAME) -t $(PROJ_NAME)/grafana:$(TAG) grafana
	docker build --no-cache --build-arg TAG=$(TAG) --build-arg PROJ_NAME=$(PROJ_NAME) -t $(PROJ_NAME)/influxdb:$(TAG) influxdb
	docker-compose build --pull --no-cache

run: build ## Build and run
	# Start using our compose file and run in the background
	docker-compose up -d

	# Start an instance of our Ansible image to perform setup on the running instance
	#  We run using the host network so that we can access not only the WSP instance, but also the individual containers.
	docker run --rm --network "host" $(PROJ_NAME)/ansible:${TAG}

	docker ps

run-nc: build-nc ## Build and run
	# Start using our compose file and run in the background
	docker-compose up -d

	# Start an instance of our Ansible image to perform setup on the running instance
	#  We run using the host network so that we can access not only the WSP instance, but also the individual containers.
	docker run --rm --network "host" $(PROJ_NAME)/ansible:${TAG}

export-nc: build-nc ## Build the images and export them
	mkdir -p images
	docker save $(PROJ_NAME)/ansible:${TAG} > images/ansible.tar
	docker save $(PROJ_NAME)/collector:${TAG} > images/collector.tar
	docker save $(PROJ_NAME)/webservices:${TAG} > images/webservices.tar
	docker save $(PROJ_NAME)/grafana:${TAG} > images/grafana.tar
#	docker save $(PROJ_NAME)/graphite:${TAG} > images/graphite.tar
	docker save $(PROJ_NAME)/influxdb:${TAG} > images/influxdb.tar

export: build ## Build the images and export them
	mkdir -p images
	docker save $(PROJ_NAME)/ansible:${TAG} > images/ansible.tar
	docker save $(PROJ_NAME)/collector:${TAG} > images/collector.tar
	docker save $(PROJ_NAME)/webservices:${TAG} > images/webservices.tar
	docker save $(PROJ_NAME)/grafana:${TAG} > images/grafana.tar
#	docker save $(PROJ_NAME)/graphite:${TAG} > images/graphite.tar
	docker save $(PROJ_NAME)/influxdb:${TAG} > images/influxdb.tar

backup-dashboards: ## Backup the Grafana dashboards and any changes made to them (Grafana must be running)
	docker run --network "host" --rm -v $(shell pwd)/backups:/home/dashboards/backup $(PROJ_NAME)/ansible:${TAG} backup.yml

migrate-graphite: ## Migrate previous Performance Analyzer Graphite database to InfluxDB (must be running)
	docker run --network "host" --rm -v $(shell pwd)/scripts:/home/scripts $(PROJ_NAME)/python-base:${TAG} /bin/sh -c "chmod +x /home/scripts/migrate.sh;/home/scripts/migrate.sh"

stop: ## Stop all of our running services
	docker-compose stop

restart: stop run ## 'stop' followed by 'run'

rm: ## Remove all existing containers defined by the project
	docker-compose rm -s -f

clean: stop rm ## Remove all images and containers built by the project
	rm -rf images
	# There are certain images created by the multi-stage builds that will not otherwise be removed. If not removed first,
	# it will cause the next commands to fail.
	docker image prune -f

	docker rmi $(PROJ_NAME)/ansible:${TAG}
	docker rmi $(PROJ_NAME)/collector:${TAG}
	docker rmi $(PROJ_NAME)/webservices:${TAG}
	docker rmi $(PROJ_NAME)/grafana:${TAG}
	docker rmi $(PROJ_NAME)/influxdb:${TAG}
	docker rmi -f $(shell docker images -q -f "label=autodelete=true")
	docker rmi -f $(shell docker images -q --filter "reference=$(PROJ_NAME)/*:${TAG}")

warn: ##
ifndef QUIET
	sh scripts/images.sh
endif
