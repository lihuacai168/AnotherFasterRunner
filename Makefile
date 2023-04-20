#.PHONY: up logs up-tag down build build-tag ps config exec restart

env := ${env}

env-file := ${HOME}/.env


# 如果外部传入了变量值，覆盖默认值
ifdef ENV_FILE
    env-file := $(ENV_FILE)
endif

compose-file := docker-compose.yml

ifdef COMPOSE_FILE
    compose-file := $(COMPOSE_FILE)
endif

cmd = docker-compose -f $(compose-file) --env-file $(env-file)


tag := $(tag)

service := $(word 1,$(MAKECMDGOALS))

.PHONY: up
up:
	$(cmd) up -d  --build --remove-orphans
	$(cmd) restart nginx
	$(cmd) restart web

.PHONY: up-no-build
up-no-build:
	$(cmd) up -d --remove-orphans
	$(cmd) restart nginx
	$(cmd) restart web

.PHONY: up-tag
up-tag:
	export TAG=$(tag); $(cmd) up -d  --build --remove-orphans
	$(cmd) restart nginx
	$(cmd) restart web


.PHONY: down
down:
	$(cmd) down

.PHONY: build
build:
	# build latest
	$(cmd) build

git-tag:
	git checkout $(tag)

.PHONY: build-tag
build-tag:git-tag
	# Build the image with the tag
	export TAG=$(tag);  $(cmd) build

.PHONY: config
config:
	$(cmd) config

.PHONY: ps
ps:
	$(cmd) ps

.PHONY: logs
logs:
	$(cmd) logs -f app celery-worker web nginx

.PHONY: restart
restart:
	$(cmd) restart $(service)

.PHONY: exec
exec:
	$(cmd) exec $(service) /bin/bash
