PYTHON=python3.10
REQUIREMENTS=requirements.txt

.PHONY: all
all: install lint test

# Create virtual environment
.PHONY: venv 
venv:
	uv venv --python=$(PYTHON)

# Delete env if available 
.PHONY: delete_env 
delete_env:
	@echo "Deleting virtual environment..."
	rm -rf .venv

# Install dependencies
.PHONY: install
install:
	uv pip install -r requirements.txt

.PHONY: run
run:
	uv run $(PYTHON) -m src.agent

# Lint code
.PHONY: lint
lint: 
	ruff check
	ruff format 
	

# Clean up
.PHONY: clean
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	