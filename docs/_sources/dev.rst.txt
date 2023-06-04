Development
===========

The project's Makefile provides many helpful shortcuts for common development tasks. Run ``make help`` for a full list of commands and their short help messages.

To add features or fixes to ``caic-python`` - please open a new pull request.

Dev Environment
---------------

Any of the :doc:`install` options that use the Makefile should setup your development environment properly. Otherwise, clone the project and run the following to get a bare minimum setup::

    make setup


Release New Version
-------------------

There is a Makefile command to help release a new version. Make sure all changes are at least commited locally because this releases everything in the current working tree. The following command builds and commits the version ``1.2.3``. This command will also generate fresh documentation and relevant Python files with version references are updated. ::

    make release VERSION=1.2.3

Ideally this will be run by a GH action eventually.
