.PHONY: build lint test

build: lint test
	poetry build

lint:
	poetry run black --check uuid25 tests
	poetry run mypy --strict uuid25 tests

test:
	poetry run python -m unittest -v
