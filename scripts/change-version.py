"""Change a project's version in pyproject.toml.

Intended to be run by Makefile, so execute from project root.
"""

import sys

import tomlkit

PYPROJECT = "pyproject.toml"

with open(PYPROJECT, "r") as fd:
    toml = tomlkit.load(fd)

    try:
        toml["project"]["version"] = sys.argv[1]
    except IndexError:
        print("Must specify a version!")
        sys.exit(1)

with open(PYPROJECT, "w") as fd:
    tomlkit.dump(toml, fd)
