Installation
============

- ``caicpy`` (will be) available on ``PyPI``, run the following to get started! ::

    pip3 install caicpy

- There are several additional installation options. With the exception of the ``curl`` command, the commands assume that you have cloned the repo and are in the repo's directory

    - An install script that uses this projects Makefile::

        curl https://raw.githubusercontent.com/gormaniac/caicpy/main/scripts/install.sh | bash

    - The Makefile (uses pipenv)::

        make setup
        make install-self

    - Build manually after cloning the repo and entering the project dir::

        pip3 install build setuptools
        python3 -m build .
        pip3 install dist/caicpy-<VERSION>.tar.gz

    - Basic install from source::

        pip3 install .