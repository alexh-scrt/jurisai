# JurisAI

JurisAI is an AI-powered legal assistant designed to help with legal research, document analysis, and case management.

## Environment Setup

```bash
# Create conda environment
conda create -n jurisai python=3.12

# Activate environment
conda activate jurisai

# Install package for development
pip install -e ".[dev]"
```

## Development

```bash
# Make sure conda environment is activated
conda activate jurisai

# Run tests
pytest

# Code formatting
black .
isort .

# Type checking
mypy src

# Linting
flake8 src
```

## Usage

JurisAI can be run in different modes:

### Using the installed package

```bash
# Run interactive mode
jurisai

# Analyze a legal document
jurisai analyze document.pdf

# Search legal database
jurisai search "legal precedent"

# Run with verbose logging
jurisai -v
```

### Using the main script directly

```bash
# Run from project root
./main.py

# Run with commands
./main.py analyze document.pdf
./main.py search "legal precedent"

# Show help
./main.py --help
```

## Project Structure

```
jurisai/
├── main.py              # Root-level script to run the application
├── src/jurisai/         # Main package code
│   ├── core/            # Core business logic
│   │   └── app.py       # Main application loop
│   ├── cli/             # Command line interface components
│   │   └── commands.py  # CLI command parsing
│   ├── api/             # API endpoints
│   ├── models/          # Data models and schemas
│   ├── utils/           # Utility functions
│   │   └── log_config.py # Structured logging setup
│   └── __init__.py      # Package initialization
├── tests/               # Test files
│   ├── test_app.py      # Core tests
│   ├── test_cli.py      # CLI tests
│   └── test_log_config.py # Logging tests
├── docs/                # Documentation
├── pyproject.toml       # Project metadata and dependencies
├── CLAUDE.md            # Development guidelines
└── README.md            # Project overview
```

## Architecture

JurisAI is structured as a modular Python application:

- **Core Module**: Contains the main application logic and business rules
- **CLI Module**: Handles command-line arguments and user interaction
- **API Module**: Provides interfaces for external services and APIs
- **Models Module**: Defines data structures and schemas
- **Utils Module**: Contains utility functions like logging
