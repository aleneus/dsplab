.PHONY: help style flakes lint uml release upload

PACKAGE = dsplab

all: help

help:
	@echo "make style"
	@echo "make flakes"
	@echo "make lint"
	@echo "make uml"
	@echo "make upload"

style:
	pycodestyle $(PACKAGE)

flakes:
	pyflakes $(PACKAGE)

lint:
	pylint $(PACKAGE)

uml:
	pyreverse $(PACKAGE) -o png

upload:
	python3 setup.py sdist upload

check:
	python3 tests/test_activity.py
	python3 tests/test_plan.py
	python3 tests/test_modulation.py
	python3 tests/test_filtration.py
	python3 tests/test_prony.py
	python3 tests/test_spectran.py
