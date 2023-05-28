"""Change a project's version in pyproject.toml.

Intended to be run by Makefile, so execute from project root.
"""

import re
import sys

import tomlkit

PYPROJECT = "pyproject.toml"
PYVERSIONRE = re.compile(r'(VERSION\=)"\d+.\d+.\d"(\n)')

try:
    NEW_VER = sys.argv[1]
except IndexError:
    print("Must specify a version!")
    sys.exit(1)

with open(PYPROJECT, "r") as fd:
    toml = tomlkit.load(fd)

    toml["project"]["version"] = NEW_VER

with open(PYPROJECT, "w") as fd:
    tomlkit.dump(toml, fd)

with open("src/caicpy/__version__.py", "r") as fd:
    data = fd.read()

    new_data = PYVERSIONRE.sub(f'\\1"{NEW_VER}"\\2', data)

with open("src/caicpy/__version__.py", "w") as fd:
    fd.write(new_data)
