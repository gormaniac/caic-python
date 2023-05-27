NAME = caicpy
PKG_DIR = src/$(NAME)

.PHONY: help
help: # Display help for all Makefile commands
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.PHONY: change-version
change-version: # Change the version of this project (requires VERSION=#.#.#)
    if [ -z "$(VERSION)" ]; then \
		echo "Must specify a VERSION argument to change the version!"; \
	else \
		pipenv run scripts/change-version.py $(VERSION)
	fi

.PHONY: build
build: # Build the package tarball and wheel
	pipenv run python3 -m build .

.PHONY: setup
setup: # Setup this project's development environment
	pipenv install -d
	pipenv run pip3 install --editable .

.PHONY: docs
docs: # Build the documentation for this package
	pipenv run sphinx-apidoc -o doc/source $(PKG_DIR)
	pipenv run sphinx-build -b html doc/source/ docs/

# .PHONY: release
# release: # Build a new versioned release and push it

.PHONY: clean
clean: # Remove build files
	rm -rf $(PKG_DIR)/__pycache__
	rm -rf src/*.egg-info
	rm -rf dist