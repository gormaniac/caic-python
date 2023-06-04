#!/bin/bash

# Intended for development installations!
# Install via "pip3 install caic_python" for standard use.

# Clone the repo, install the pipenv, and install the package to the pipenv.
# Will require git, make, and pipenv.

git clone https://github.com/gormaniac/caic_python.git
cd caic_python
make setup
make install-self
