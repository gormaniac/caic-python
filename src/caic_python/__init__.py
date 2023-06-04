"""The ``caic-python`` module.

Also defines ``__version__``:

The current version of ``caic-python`` - set by ``make change-version``.

Must map to ``pyproject.toml``'s version. Using ``make change-version``
or ``scripts/change-version.py`` ensures this.
"""

import logging

__version__ = "0.1.10"

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
"""The logger used by ``caic-python``, by default the level is ``logging.WARNING``.

Callers may change the logging level by importing ``LOGGER``.
"""
