# Variables
VENV = .venv
PYTHON = $(VENV)/Scripts/python
TEST_DIR = tests

# Default target
all: install lint test

# Set up virtual environment with uv
venv:
	$(PYTHON) -m venv $(VENV)
	$(PYTHON) -m pip install -U uv

# Install dependencies with uv (faster than pip)
install: venv
	$(UV) pip install -r requirements-dev.txt
	$(UV) pip install -e .

# Format code with Black
format:
	black .

# Run linter (Ruff) with auto-fix
lint:
	$(RUFF) check . --fix

# Run type checker (Mypy)
typecheck:
	$(MYPY) .

# Run tests with pytest
test:
	$(PYTHON) -m pytest -v $(TEST_DIR)

# Run tests with coverage
coverage:
	$(PYTHON) -m pytest --cov=. --cov-report=html $(TEST_DIR)
	@echo "Coverage report: file://$(abspath htmlcov/index.html)"

# Clean up
clean:
	rm -rf `find . -type d -name __pycache__`
	rm -rf .mypy_cache .pytest_cache htmlcov

# Full CI pipeline
ci: install lint typecheck test

# Development workflow (watch mode, requires 'entr')
watch:
	find . -name '*.py' | entr -c make lint typecheck test

.PHONY: all venv install format lint typecheck test coverage clean ci watch