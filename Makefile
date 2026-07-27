PYTHON ?= python3

.PHONY: test quality demo

test:
	$(PYTHON) -m pytest

quality:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m ruff format --check .

demo:
	PYTHONPATH=src $(PYTHON) -m carryover_football \
		examples/data/synthetic_origin_role.json \
		examples/data/synthetic_destination_role.json
