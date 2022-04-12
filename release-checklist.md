# Release checklist

## Code

* Check is ok: `make check`
* Test coverage is not less than 71%: `make check`
* The result of pylint is not less than 9.9: `make lint`
* Version in source code is updated: `make ver`
* Old deprecated code is removed: see todo list

## Demo

* The result of pylint is not less than 8.55: `make lint-demo`
* All examples work: `./run-demo.sh`

## Docs

* Docs is successfully built: `make docs`
* History is updated in docs: `head -n 20 docs/source/history.rst`

## Installation

* All dependencies are relevant in setup.py
* Installation successful: `python3 setup.py install --user`
* Example from README.md works after installation
