COMPOSE = docker-compose -p cookiecutter_tartiflette_aiohttp


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
