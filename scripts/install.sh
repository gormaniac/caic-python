#!/bin/bash

# Intended for development installations!
# Install via "pip3 install caicpy" for standard use.

# Clone the repo, install the pipenv, and install the package to the pipenv.
# Will require git, make, and pipenv.

git clone https://github.com/gormaniac/caicpy.git
cd caicpy
make setup
make install-self
