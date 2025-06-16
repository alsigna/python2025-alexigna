.PHONY: lint init-dev

init:
	pip install poetry
	poetry install --without dev

init-dev: init
	poetry install --with dev

build: init
	poetry build

lint:
	poetry run black --check .

check: lint
	@echo "✅ Проверки пройдены"