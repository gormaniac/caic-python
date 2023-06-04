#!/bin/bash

# Intended for development installations!
# Install via "pip3 install caic-python" for standard use.

# Clone the repo, install the pipenv, and install the package to the pipenv.
# Will require git, make, and pipenv.

git clone https://github.com/gormaniac/caic-python.git
cd caic-python
make setup
make install-self
