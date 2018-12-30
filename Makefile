.DEFAULT_GOAL := all

.PHONY: install, typecheck, fmt, fmt-check, test, clean, build, install-program, publish, ci

install:
	poetry install

typecheck:
	poetry run mypy .

fmt:
	poetry run black .

fmt-check:
	poetry run black . --check

lint: fmt-check typecheck

test:
	poetry run pytest

clean:
	rm -rf dist *.egg-info

build: clean
	poetry build

install-program: build
	python3 -m pip install dist/awsudo-py-*.tar.gz 

uninstall-program:
	python3 -m pip uninstall awsudo-py

publish: build
	poetry publish

all: lint test build
