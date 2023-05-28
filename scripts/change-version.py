"""Change a project's version in pyproject.toml.

Intended to be executed from project root.
"""

import re
import sys

import tomlkit

PYPROJECT = "pyproject.toml"
PKGINIT = "src/caicpy/__init__.py"

PYVERSIONRE = re.compile(r'(__version__\s?\=\s?)".+"(\n)')

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

with open(PKGINIT, "r") as fd:
    data = fd.read()

    new_data = PYVERSIONRE.sub(f'\\1"{NEW_VER}"\\2', data)

with open(PKGINIT, "w") as fd:
    fd.write(new_data)
