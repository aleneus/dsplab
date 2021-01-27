# Release checklist

## Code

* No `TODO` in code
* The result of pylint is not less than 9.75 (make lint)
* No errors from pylint (make lint-e)
* No flakes (make flake)
* Version in source code is updated
* Old deprecated code is removed (see todo list)
* All unit tests passed (make check)
* Total test coverage is not less than 47%

## Demo

* The result of pylint is not less than 8.55 (make lint-demo)
* All examples work

## Docs

* All necessary modules are included to docs
* History is updated in docs
* Docs is successfully built (make docs)

## Installation

* All dependencies are relevant in setup.py
* Installation successful (python3 setup.py install --user)
* Example from README.md works after installation
