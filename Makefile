.DEFAULT_GOAL := all

.PHONY: typecheck
typecheck:
	poetry run mypy .

.PHONY: fmt
fmt:
	poetry run black .

.PHONY: test
test:
	poetry run pytest

.PHONY: clean
clean:
	rm -f awsudo-py-*.tar.gz awsudo-py-*.whl

.PHONY: build
build: clean
	poetry build

.PHONY: ci
# error on bad formatting
ci: typecheck test
	poetry run black . --check

all: fmt typecheck build
