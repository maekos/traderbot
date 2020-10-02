# the command to invoke fades
FADES := fades -d docker-compose==1.19.0 -x
# the command to invoke docker-compose
COMPOSE := $(FADES) docker-compose

help:
	@echo "help             -- print this help"
	@echo "build            -- build docker environment"
	@echo "stop             -- stop docker stack"
	@echo "clean            -- clean all artifacts"
	@echo "down             -- stop compose (all containers)"
	@echo "shell      		-- run bash inside coke docker"
	@echo "check_style      -- run code linting tools"

build:
	$(COMPOSE) build

stop:
	$(COMPOSE) stop

clean: stop
	$(COMPOSE) rm --force

run:
	$(COMPOSE) run --rm trader /bin/bash -c bin/traderbot
	$(MAKE) down

down:
	${COMPOSE} down -v --remove-orphans

${SINGLE_TEST}:
	$(COMPOSE) run tester ./run_tests $(@).py
	$(MAKE) down

shell:
	$(COMPOSE) run --rm trader /bin/bash
	$(MAKE) down

check_style:
	docker run -ti --rm -v $(PWD):/apps alpine/flake8:3.5.0 trader --statistics --benchmark

.PHONY: help build stop clean down run shell check_style
