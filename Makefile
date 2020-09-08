.PHONY: docs

PACKAGE_FOLDER = dsplab
DEMO_FOLDER = demo

all: help

help:
	@echo "make check"
	@echo "make cover"
	@echo "make style"
	@echo "make flakes"
	@echo "make lint"
	@echo "make lint-demo"
	@echo "make uml"
	@echo "make docs"
	@echo "make upload"
	@echo "make clear"


check:
	@nose2 -vvv

cover:
	@nose2 --with-coverage --coverage-report=html

style:
	pycodestyle $(PACKAGE_FOLDER)

flakes:
	pyflakes $(PACKAGE_FOLDER)

lint:
	pylint $(PACKAGE_FOLDER)

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
