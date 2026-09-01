.PHONY: help install run test clean

help:
	@echo "Blacksmith Project - Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make install   Install dependencies"
	@echo "  make run       Run the service"
	@echo "  make test      Run tests"
	@echo "  make clean     Remove generated files"
	@echo ""

install:
	pip install -e .

run:
	blacksmith-service

test:
	python -m pytest tests/ -v

clean:
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete