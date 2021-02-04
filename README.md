# dsplab package

## Fields of application

* Development of software for digital signal processing.
* Development of the DSP routines that require a flexible configuration of different stages of calculations on the user level.
* Investigation of variety of methods solving the same DSP task.

## Features and characteristics

* Some specific functions for analysis of signals.
* Synthesis of test signals with different kinds of **modulation**: amplitude, frequency and phase.
* **Playing** of signals (synthesized or archive) for the development of on-line procedures.
* Organization of calculations, **workflows**:
    - User can define the **plan of works** and then set the **worker** for every work. The replacement of the worker does not destroy the workflow.
    - Different types of nodes are supported: **Work**, **Map (Loop)**, **Select** and **Pack**.
    - Base classes for workers are defined. Every worker can return detailed description of itself by calling **info()** method.
    - Base class for on-line filters having **add_sample()** method and embedded **queues** for running window and smoothing of results is implemented.
* Licence: **LGPLv3**
* Programming language: **Python 3**.

## Installation

```bash
pip install dsplab
```

## Example

File `workers.py`:

```python
class Add:
    def __init__(self, value):
        self.value = value

    def __call__(self, x):
        return x + self.value
```

File `main.py`:

```python
import json
from dsplab.flow.plan import get_plan_from_dict

with open('plan.json') as buf:
    conf = json.loads(buf.read())

p = get_plan_from_dict(conf)

x = 1
y = p([x, ])
print(y)
```

File `plan.json`:

```json
{
    "nodes": [
        {
            "id": "a",
            "class": "WorkNode",
            "work": {
                "descr": "Increase input value",
                "worker": {
                    "class": "workers.Add",
                    "params": {"value": 1}
                }
            }
        }
    ],

    "inputs": ["a"],
    "outputs": ["a"]
}
```

## Documentation

http://dsplab.readthedocs.io/en/latest/
