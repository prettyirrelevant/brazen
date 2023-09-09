LINT_PATHS = apps/ services/ brazen/ common/ manage.py

include .env.dev

lint:
	isort $(LINT_PATHS) --diff --check-only
	ruff $(LINT_PATHS)

format:
	isort $(LINT_PATHS)
	ruff $(LINT_PATHS) --fix
	black $(LINT_PATHS)

runserver:
	@echo 'Running brazen development server...'
	python -X dev manage.py runserver