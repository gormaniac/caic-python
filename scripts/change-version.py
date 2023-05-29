"""Change a project's version in pyproject.toml.

Intended to be executed from project root.
"""

import re
import sys

import tomlkit

PYPROJECT = "pyproject.toml"
with open(PYPROJECT, "r") as fd:
    toml = tomlkit.load(fd)

PKGINIT = f"src/{toml['project']['name']}/__init__.py"
PYVERSIONRE = re.compile(r'(__version__\s?\=\s?)".+"(\n)')

try:
    NEW_VER = sys.argv[1]
except IndexError:
    print("Must specify a version!")
    sys.exit(1)

with open(PYPROJECT, "w") as fd:
    toml["project"]["version"] = NEW_VER
    tomlkit.dump(toml, fd)

with open(PKGINIT, "r") as fd:
    data = fd.read()
    new_data = PYVERSIONRE.sub(f'\\1"{NEW_VER}"\\2', data)

with open(PKGINIT, "w") as fd:
    fd.write(new_data)
