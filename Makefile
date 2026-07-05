.PHONY: help install dev test lint format clean docs run

help:
	@echo "PDA Voice Monitor - Development Tasks"
	@echo "====================================="
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install     Install production dependencies"
	@echo "  dev         Install development dependencies"
	@echo "  venv        Create virtual environment"
	@echo "  test        Run test suite"
	@echo "  lint        Run code quality checks"
	@echo "  format      Auto-format code with Black"
	@echo "  clean       Remove build artifacts and cache"
	@echo "  run         Run the monitor"
	@echo "  run-once    Run once and check current state"
	@echo "  docs        Generate documentation"
	@echo "  publish     Build and publish to PyPI"
	@echo ""

venv:
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip

install: venv
	. venv/bin/activate && pip install -r requirements.txt

dev: install
	. venv/bin/activate && pip install -e ".[dev]"

test:
	. venv/bin/activate && pytest tests/ -v --cov=pda --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

lint:
	. venv/bin/activate && \
		echo "Running flake8..." && \
		flake8 pda/ tests/ main.py && \
		echo "Running mypy..." && \
		mypy pda/ tests/ main.py --ignore-missing-imports

format:
	. venv/bin/activate && \
		echo "Formatting with Black..." && \
		black pda/ tests/ main.py --line-length=100

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ htmlcov/ .coverage .pytest_cache .tox .mypy_cache

run:
	. venv/bin/activate && python main.py

run-once:
	. venv/bin/activate && python main.py --once

run-verbose:
	. venv/bin/activate && python main.py --verbose

docs:
	@echo "Generating documentation..."
	@mkdir -p docs
	. venv/bin/activate && python -m pdoc --html --output-dir docs pda
	@echo "Documentation generated in docs/ directory"

publish: clean
	. venv/bin/activate && \
		pip install build twine && \
		python -m build && \
		twine upload dist/*

.PHONY: all
all: clean dev lint test
	@echo "✓ All checks passed!"
