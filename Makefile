NAME = caicpy
PKG_DIR = src/$(NAME)

.PHONY: help
help: # Display help for all Makefile commands
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.PHONY: change-version
change-version: # Change the version of this project (requires VERSION=#.#.#)
	pipenv run python3 scripts/change-version.py $(VERSION)

.PHONY: build
build: # Build the package tarball and wheel
	pipenv run python3 -m build .

.PHONY: setup
setup: # Setup this project's pipenv environment
	pipenv install -d

.PHONY: install-self
install-self: # Install this project's python package using the pipenv's pip
	pipenv run pip3 install --editable .

.PHONY: docs
docs: # Build the documentation for this package
	pipenv run sphinx-apidoc -o doc/source $(PKG_DIR)
	pipenv run sphinx-build -b html doc/source/ docs/

.PHONY: clean
clean: # Remove build files - including a forced git rm of dist/*
	rm -rf $(PKG_DIR)/__pycache__
	rm -rf src/*.egg-info
	git rm -f dist/*
	rm -rf dist

.PHONY: release
release: change-version clean setup build docs # Build a new versioned release and push it (requires VERSION=#.#.#)
	git add dist/* docs/* docs/.doctrees docs/.buildinfo pyproject.toml $(PKG_DIR)/__version__.py
	git commit -m "build: release v$(VERSION)"
	git push
	git tag -a v$(VERSION) -m "Release v$(VERSION)"
	git push origin v$(VERSION)
