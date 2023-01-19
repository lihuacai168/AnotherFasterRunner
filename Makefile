#.PHONY: up logs up-tag down build build-tag ps config exec restart

env := ${env}

env-file := ${HOME}/.env

cmd = docker-compose -f docker-compose.yml --env-file $(env-file)


tag := $(tag)

service := $(word 1,$(MAKECMDGOALS))

.PHONY: up
up:
	$(cmd) up -d  --build --remove-orphans
	$(cmd) restart nginx

.PHONY: up-tag
up-tag:
	export TAG=$(tag); $(cmd) up -d  --build --remove-orphans
	$(cmd) restart nginx


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
	$(cmd) exec $(service) /bin/sh