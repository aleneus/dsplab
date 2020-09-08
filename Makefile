.PHONY: help style flakes lint uml release upload

PACKAGE_FOLDER = dsplab
DEMO_FOLDER = demos

all: help

help:
	@echo "make check"
	@echo "make cover"
	@echo "make style"
	@echo "make flakes"
	@echo "make lint"
	@echo "make lint-demo"
	@echo "make uml"
	@echo "make upload"


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

upload:
	python3 setup.py sdist upload
