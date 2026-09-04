VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
STAMP := $(VENV)/.installed

.PHONY: help install run test clean

help:
	@echo "Blacksmith Project - Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make install   Create venv and install dependencies (including dev)"
	@echo "  make run       Run the service"
	@echo "  make test      Run tests"
	@echo "  make clean     Remove generated files"
	@echo ""

install: $(STAMP)

$(STAMP): pyproject.toml
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"
	@touch $(STAMP)

run: $(STAMP)
	$(VENV)/bin/blacksmith-service

test: $(STAMP)
	$(PYTHON) -m pytest tests/ -v

clean:
	rm -rf build/ dist/ *.egg-info $(VENV)
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
