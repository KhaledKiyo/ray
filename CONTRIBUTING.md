# Contributing to PDA Voice Monitor

Thank you for your interest in contributing! Here's how to help:

## Development Setup

```bash
# Clone the repository
git clone <repo-url>
cd ray

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install with dev dependencies
pip install -e ".[dev]"
```

## Code Style

We use Black for code formatting:

```bash
black pda/ tests/ main.py
```

## Linting

Check code quality:

```bash
flake8 pda/ tests/ main.py
mypy pda/ tests/ main.py
```

## Testing

Run the test suite:

```bash
pytest tests/ -v
pytest tests/ --cov=pda --cov-report=html
```

## Submitting Changes

1. Create a branch: `git checkout -b fix/issue-123`
2. Make changes and add tests
3. Run tests and linting
4. Commit: `git commit -am 'Fix: description'`
5. Push: `git push origin fix/issue-123`
6. Open a pull request

## Commit Message Format

- `feat: Add new feature`
- `fix: Fix bug`
- `docs: Update documentation`
- `test: Add tests`
- `refactor: Improve code structure`

## Reporting Bugs

Include:
- Python version
- Linux distribution
- Error message and traceback
- Steps to reproduce

## Feature Requests

Describe:
- Use case
- Expected behavior
- Why it would be useful
