# Release checklist

## Code

* No `TODO` in code
* All unit tests passed (make check)
* Total test coverage is not less than 44%
* No flakes (make flake)
  - Note: unused imports are allowed in deprecated modules
* The result of pylint is not less than 9.65 (make lint)
* No errors from pylint (make lint-e)
* Version in source code is updated
* All dependencies are relevant in setup.py

## Demo

* All examples work
* The result of pylint is not less than 8.5 (make lint-demo)

## Docs

* Docs is successfully built (make docs)
* All necessary modules are included to docs
* History is updated in docs

## Installation

* Installation successful (python3 setup.py install --user)
