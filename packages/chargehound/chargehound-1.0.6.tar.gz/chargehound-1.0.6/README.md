# Chargehound python bindings 

[![Build Status](https://travis-ci.org/chargehound/chargehound-python.svg?branch=master)](https://travis-ci.org/chargehound/chargehound-python) [![PyPI version](https://badge.fury.io/py/chargehound.svg)](https://badge.fury.io/py/chargehound)

## Installation

`pip install chargehound`

## Usage

Import chargehound and set your API key.

```python
import chargehound
chargehound.api_key = '{ YOUR_API_KEY }'
```

## Documentation

[Disputes](https://www.chargehound.com/docs/api/index.html?python#disputes)

[Errors](https://www.chargehound.com/docs/api/index.html?python#errors)

## Development

To build and install from the latest source:

```bash
$ git clone git@github.com:chargehound/chargehound-python.git
$ pip install -r dev_requirements.txt
```

Run tests:

```bash
$ python setup.py test
```
