.PHONY: build lint test

build: lint test
	poetry build

lint:
	black --check uuid25 tests
	mypy --strict uuid25 tests

test:
	python -m unittest -v
