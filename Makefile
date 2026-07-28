# Interpreter used to create the virtualenv. Override to test another version:
#   make setup PYTHON=python3.13
PYTHON ?= python3

VENV := .venv
VENV_PYTHON := $(VENV)/bin/python

.PHONY: setup test quality demo learn

# The virtualenv interpreter is a real file, so make can treat it as a build
# target: it is created when missing and refreshed whenever pyproject.toml
# changes, which is how new dependencies get picked up. Every other target
# depends on it, so a clean clone can run any command in any order.
#
# The venv is only CREATED when missing. A dependency change reinstalls into the
# existing venv using its own interpreter, so editing pyproject.toml never
# re-triggers the version guard below and never needs PYTHON= passing again.
$(VENV_PYTHON): pyproject.toml
	@if [ ! -x "$(VENV_PYTHON)" ]; then \
		$(PYTHON) -c 'import sys; sys.exit(sys.version_info < (3, 12))' || { \
			echo "Carryover requires Python 3.12+, but '$(PYTHON)' is $$($(PYTHON) -V 2>&1)."; \
			echo "Retry with an explicit interpreter, for example:"; \
			echo "    make setup PYTHON=python3.12"; \
			exit 1; \
		}; \
		$(PYTHON) -m venv $(VENV); \
	fi
	$(VENV_PYTHON) -m pip install --quiet --upgrade pip
	$(VENV_PYTHON) -m pip install --quiet --editable '.[dev]'
	touch $@

setup: $(VENV_PYTHON)
	@echo "Environment ready. Next: make quality, make test, make demo"

test: $(VENV_PYTHON)
	$(VENV_PYTHON) -m pytest

quality: $(VENV_PYTHON)
	$(VENV_PYTHON) -m ruff check .
	$(VENV_PYTHON) -m ruff format --check .

demo: $(VENV_PYTHON)
	$(VENV_PYTHON) -m carryover_football \
		examples/data/synthetic_origin_role.json \
		examples/data/synthetic_destination_role.json

learn: $(VENV_PYTHON)
	$(VENV_PYTHON) learning/01_sampling_variance.py
	$(VENV_PYTHON) learning/02_distance_metrics.py
	$(VENV_PYTHON) learning/03_percentiles_and_zscores.py
