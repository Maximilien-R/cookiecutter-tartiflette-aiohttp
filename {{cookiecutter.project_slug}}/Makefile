COMPOSE = docker-compose -p {{cookiecutter.project_slug}}


.PHONY: init
init:
	# This following command is used to provision the network
	$(COMPOSE) up --no-start --no-build app | true


.PHONY: run
run:
	$(COMPOSE) build app
	$(COMPOSE) up app


.PHONY: down
down:
	$(COMPOSE) down


.PHONY: clean
clean:
	$(COMPOSE) down --volumes --rmi=local


.PHONY: format-imports
format-imports:
	$(COMPOSE) build format-imports
	$(COMPOSE) run format-imports


.PHONY: format
format: format-imports
	$(COMPOSE) build format
	$(COMPOSE) run format


.PHONY: check-imports
check-imports:
	$(COMPOSE) build check-imports
	$(COMPOSE) run check-imports


.PHONY: check-format
check-format:
	$(COMPOSE) build check-format
	$(COMPOSE) run check-format


.PHONY: style
style: check-imports check-format
	$(COMPOSE) build style
	$(COMPOSE) run style


.PHONY: complexity
complexity:
	$(COMPOSE) build complexity
	$(COMPOSE) run complexity


.PHONY: security-sast
security-sast:
	$(COMPOSE) build security-sast
	$(COMPOSE) run security-sast


.PHONY: test-unit
test-unit:
	$(COMPOSE) build test-unit
	$(COMPOSE) run test-unit


.PHONY: test-functional
test-functional:
	$(COMPOSE) build test-functional
	$(COMPOSE) run test-functional


.PHONY: test
test: test-unit test-functional
