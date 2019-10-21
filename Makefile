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


##
# plugin targets
##
run-plugins: build-plugins ## Build and run plugins
	$(shell ./scripts/plugin_compose_info.sh "up -d")

build-plugins: ## Build all plugins
	$(shell PROJ_NAME=$(PROJ_NAME) ./scripts/plugin_build_info.sh)

stop-plugins: ## Stop all plugins
	$(shell ./scripts/plugin_compose_info.sh "stop")

down-plugins: ## Run docker-compose down on all plugins
	$(shell ./scripts/plugin_compose_info.sh "down")

clean-plugins: ## Remove all images built by plugins
	$(shell PROJ_NAME=$(PROJ_NAME) ./scripts/plugin_remove_info.sh)


# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help warn

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

# DOCKER TASKS
# Build the container
build: __docker-find warn ## Build the container
	docker build --build-arg REPO_FILE=$(ALPINE_REPO_FILE) --build-arg TAG=$(TAG) -t $(PROJ_NAME)/alpine-base:${TAG} build/alpine
	docker build --build-arg PIP_CONF=$(PIP_CONF) --build-arg TAG=$(TAG) --build-arg PROJ_NAME=$(PROJ_NAME) -t $(PROJ_NAME)/python-base:${TAG} build/python
	docker build --build-arg TAG=$(TAG) --build-arg PROJ_NAME=$(PROJ_NAME) -t $(PROJ_NAME)/ansible:${TAG} ansible
	docker build --build-arg TAG=$(TAG) --build-arg PROJ_NAME=$(PROJ_NAME) -t $(PROJ_NAME)/influxdb:$(TAG) influxdb
	docker build --build-arg TAG=$(TAG) --build-arg PROJ_NAME=$(PROJ_NAME) -t $(PROJ_NAME)/grafana:$(TAG) grafana
	docker-compose build

build-nc: __docker-find warn ## Build the container without caching
	docker build --no-cache -f build/alpine/Dockerfile --build-arg REPO_FILE=$(ALPINE_REPO_FILE) --build-arg TAG=$(TAG) -t $(PROJ_NAME)/alpine-base:${TAG} build/alpine
	docker build --no-cache -f build/python/Dockerfile --build-arg PIP_CONF=$(PIP_CONF) --build-arg TAG=$(TAG) --build-arg PROJ_NAME=$(PROJ_NAME) -t $(PROJ_NAME)/python-base:${TAG} build/python
	docker build --no-cache --build-arg TAG=$(TAG) --build-arg PROJ_NAME=$(PROJ_NAME) -t $(PROJ_NAME)/ansible:${TAG} ansible
	docker build --no-cache --build-arg TAG=$(TAG) --build-arg PROJ_NAME=$(PROJ_NAME) -t $(PROJ_NAME)/influxdb:$(TAG) influxdb
	docker build --no-cache --build-arg TAG=$(TAG) --build-arg PROJ_NAME=$(PROJ_NAME) -t $(PROJ_NAME)/grafana:$(TAG) grafana
	docker-compose build --pull --no-cache

run: build build-plugins ## Build and run
	# Start using our compose file and run in the background
	docker-compose up -d 

	# Start an instance of our Ansible image to perform setup on the running instance
	docker run --rm --network=container:grafana $(PROJ_NAME)/ansible:${TAG}

	make run-plugins
	docker ps

run-nc: build-nc ## Build and run
	# Start using our compose file and run in the background
	docker-compose up -d 

	# Start an instance of our Ansible image to perform setup on the running instance
	docker run --rm --network=container:grafana $(PROJ_NAME)/ansible:${TAG}

	make run-plugins
	docker ps

export-nc: build-nc ## Build the images and export them
	mkdir -p images
	docker save $(PROJ_NAME)/ansible:${TAG} > images/ansible.tar
	docker save $(PROJ_NAME)/influxdb:${TAG} > images/influxdb.tar
	docker save $(PROJ_NAME)/grafana:${TAG} > images/grafana.tar

export: build ## Build the images and export them
	mkdir -p images
	docker save $(PROJ_NAME)/ansible:${TAG} > images/ansible.tar
	docker save $(PROJ_NAME)/influxdb:${TAG} > images/influxdb.tar
	docker save $(PROJ_NAME)/grafana:${TAG} > images/grafana.tar

stop: __docker-find ## Stop all of our running services
	docker-compose stop
	make stop-plugins

restart: stop run ## 'stop' followed by 'run'

rm: __docker-find ## Remove all existing containers defined by the project
	docker-compose rm -s -f
	$(shell ./scripts/plugin_compose_info.sh "rm -s -f")

clean: stop rm ## Remove all images and containers built by the project
	rm -rf images
	# There are certain images created by the multi-stage builds that will not otherwise be removed. If not removed first,
	# it will cause the next commands to fail.
	docker image prune -f

	docker rmi $(PROJ_NAME)/ansible:${TAG}
	docker rmi $(PROJ_NAME)/influxdb:${TAG}
	docker rmi $(PROJ_NAME)/grafana:${TAG}
	docker rmi -f $(shell docker images -q -f "label=autodelete=true")
	docker rmi -f $(shell docker images -q --filter "reference=$(PROJ_NAME)/*:${TAG}")
	make clean-plugins

warn: ##
ifndef QUIET
	@chmod +x scripts/*
	@scripts/images.sh
endif

__docker-find: ##
	@chmod +x scripts/*
	@scripts/docker_exists.sh
