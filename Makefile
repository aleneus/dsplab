.PHONY: help style flakes lint uml release upload

PACKAGE = dsplab

all: help

help:
	@echo "make style"
	@echo "make flakes"
	@echo "make lint"
	@echo "make uml"
	@echo "make release ver=value"
	@echo "make upload"

style:
	pycodestyle $(PACKAGE)

flakes:
	pyflakes $(PACKAGE)

lint:
	pylint $(PACKAGE)

uml:
	pyreverse $(PACKAGE) -o png

release:
	@echo $(ver)
	hg up default
	@echo 'Update to default: OK'
	hg merge develop
	@echo 'Merge from develop: OK'
	hg ci -m 'merge from develop'
	hg tag $(ver)
	@echo 'Add tag: OK'
	hg up develop
	@echo 'Update to develop: OK'

upload:
	python3 setup.py sdist upload
