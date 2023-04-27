#.PHONY: up logs up-tag down build build-tag ps config exec restart

env := ${env}

HOME_ENV := ${HOME}/.env
CURRENT_ENV := .env.example
env-file := $(CURRENT_ENV)

ifndef ENV_FILE
	ifneq ($(wildcard $(HOME_ENV)),)
		env-file := $(HOME_ENV)
	else
		WARN_MSG := $(warning WARNING: ${HOME_ENV} not found and no ENV_FILE provided, using .env.example instead)
	endif
else
	env-file := $(ENV_FILE)
endif

compose-file := docker-compose.yml

ifdef COMPOSE_FILE
    compose-file := $(COMPOSE_FILE)
endif

cmd = docker-compose -f $(compose-file) --env-file $(env-file)


tag := $(tag)

service := $(word 1,$(MAKECMDGOALS))

.PHONY: fastup
fastup:
	docker-compose -f docker-compose-for-fastup.yml --env-file .env.example up -d --build --remove-orphans
	docker-compose -f docker-compose-for-fastup.yml --env-file .env.example restart nginx web

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
