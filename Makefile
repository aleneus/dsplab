.PHONY: docs test

PACKAGE_FOLDER = dsplab
DEMO_FOLDER = demo

all: help

help:
	@echo "check"
	@echo "cover"
	@echo "lint"
	@echo "lint-demo"
	@echo "ver"
	@echo "uml"
	@echo "docs"
	@echo "upload"
	@echo "clear"


check: test todo flake lint-e

test:
	@nose2 -vvv --with-coverage

todo:
	@rgrep "TODO" --include="*py" --exclude-dir="env" || true
	@rgrep "TODO" --include="*rst" || true
	@rgrep "TODO" --include="*md" --exclude="release-checklist.md" || true
	@rgrep "# REF" --include="*py" || true

flake:
	flake8 $(PACKAGE_FOLDER)

lint-e:
	pylint --disable=R,C,W $(PACKAGE_FOLDER) || true

cover:
	@nose2 --with-coverage --coverage-report=html

lint:
	pylint $(PACKAGE_FOLDER) || true

lint-demo:
	pylint $(DEMO_FOLDER)

docs:
	sphinx-build docs/source/ docs/build/

ver:
	@cat $(PACKAGE_FOLDER)/__init__.py | grep __version__

uml:
	pyreverse $(PACKAGE_FOLDER) -o png

upload:
	python3 setup.py sdist
	python3 -m twine upload --repository pypi dist/*

clear:
	@rm -rf htmlcov/
	@rm -rf docs/build/
