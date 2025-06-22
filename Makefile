.PHONY: lint init-dev

init:
	pip install poetry
	poetry install --without dev

init-dev: init
	poetry install --with dev

build: init
	poetry build

lint:
	poetry run black --check src
	poetry run ruff check src
	poetry run flake8 src

mypy:
	poetry run mypy src

check: lint mypy
	@echo "✅ Проверки пройдены"