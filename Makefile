.PHONY: lint init-dev

init-dev:
	poetry install --with dev

lint:
	poetry run black --check .

check: lint
	@echo "✅ Проверки пройдены"