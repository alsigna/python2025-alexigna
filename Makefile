.PHONY: lint

lint:
	poetry run black .

check: lint
	@echo "✅ Проверки пройдены"