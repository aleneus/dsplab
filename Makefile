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
	hg merge develop
	hg ci -m 'merge from develop'
	hg tag $(ver)
	hg up develop

upload:
	python3 setup.py sdist upload
