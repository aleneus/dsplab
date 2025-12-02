.PHONY: docs test

PACKAGE_FOLDER = dsplab
DEMO_FOLDER = demo

check: test todo lint-e

test:
	@nose2 -vvv --with-coverage

todo:
	@grep -rn "TODO" --include="*py" --exclude-dir="env" || true
	@grep -rn "TODO" --include="*rst" || true
	@grep -rn "TODO" --include="*md" --exclude="release-checklist.md" || true

lint-e:
	pylint --disable=R,C,W $(PACKAGE_FOLDER) || true

cover:
	@nose2 --with-coverage --coverage-report=html

lint:
	pylint $(PACKAGE_FOLDER) || true

lint-demo:
	pylint $(DEMO_FOLDER) || true

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
