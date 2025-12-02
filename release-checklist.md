# Release checklist

## Code

* Test ok, coverage >= 72%: `make check`
* The result of pylint is not less than 9.9: `make lint`
* Version in source code is updated: `dsplab/__init__.py`

## Demo

* All examples work: `./run-demo.sh`
* The result of pylint is not less than 9.7: `make lint-demo`

## Docs

* History is updated: `docs/source/history.rst`
* Docs is successfully built: `make docs`
* License is relevant: `LICENSE`

## Installation

* All dependencies are relevant in `setup.py`
* Installation successful: use separate virtual environement
* Example from README.md works after installation
