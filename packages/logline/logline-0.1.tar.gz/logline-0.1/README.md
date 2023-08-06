# LogLine-Python
LogLine is an entirely web-based logging platform. This Python library interfaces with it to allow you to utilise LogLine in your Python applications.

## Installation
The recommended way to install LogLine-Python is to use [PyPI](https://pypi.python.org/):

```
pip install logline
```

## Example usage

```python
from logline import *

logline = LogLine("DF165TEZIC")

if logline.info("test logging from python"):
	print("Info log succeeded")
if logline.success("test logging from python"):
	print("Success log succeeded")
if logline.warning("test logging from python"):
	print("Warning log succeeded")
if logline.fatal("test logging from python"):
	print("Fatal log succeeded")
```

## Tests

There is a [test script](logline/tests/test.py) included for testing purposes, it may prove useful, or it may not.