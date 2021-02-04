.PHONY: docs

PACKAGE_FOLDER = dsplab
DEMO_FOLDER = demo

all: help

help:
	@echo "check"
	@echo "cover"
	@echo "flake"
	@echo "lint"
	@echo "lint-e"
	@echo "lint-demo"
	@echo "uml"
	@echo "docs"
	@echo "upload"
	@echo "clear"


check:
	@nose2 -vvv --with-coverage

cover:
	@nose2 --with-coverage --coverage-report=html

flake:
	flake8 $(PACKAGE_FOLDER)

lint:
	pylint $(PACKAGE_FOLDER)

lint-e:
	pylint --disable=R,C,W $(PACKAGE_FOLDER)

lint-demo:
	pylint $(DEMO_FOLDER)

uml:
	pyreverse $(PACKAGE_FOLDER) -o png

docs:
	sphinx-build docs/source/ docs/build/


upload:
	python3 setup.py sdist upload

clear:
	@rm -rf htmlcov/
	@rm -rf docs/build/
