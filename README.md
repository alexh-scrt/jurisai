# JurisAI

JurisAI is an AI-powered legal assistant designed to help with legal research, document analysis, and case management.

## Environment Setup

### Option 1: Using pip with requirements.txt

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Option 2: Using conda

```bash
# Create conda environment
conda create -n jurisai python=3.12

# Activate environment
conda activate jurisai

# Install requirements
pip install -r requirements.txt

# Or install package for development
pip install -e ".[dev]"
```

### Option 3: Using the package locally

```bash
# Install the package in development mode
pip install -e .
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

# Launch web interface
jurisai web

# Launch web interface on a specific port
jurisai web --port 8502

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

# Launch web interface
./main.py web

# Run with commands
./main.py analyze document.pdf
./main.py search "legal precedent"

# Show help
./main.py --help
```

## Web Interface

JurisAI includes a web interface built with Streamlit that allows you to:

1. Upload legal documents (PDF files)
2. Process and analyze the documents using semantic chunking
3. Ask questions about the documents and get AI-generated answers

### Prerequisites

Before using the web interface, make sure you have Ollama installed and running:

1. Install Ollama from https://ollama.ai/
2. Pull the required model:
   ```bash
   ollama pull deepseek-r1:1.5b
   ```
   (You can also use other supported models like llama2:7b, mistral:7b, etc.)

### Starting the Web Interface

1. Launch the web application:
   ```bash
   jurisai web
   ```

2. Open your browser and navigate to http://localhost:8501

3. Upload a PDF document and ask questions about its content

### Technologies Used

The web interface uses:
- **Hugging Face Embeddings** for semantic text processing
- **FAISS Vector Store** for efficient similarity search
- **Ollama** for running local LLMs to generate answers
- **Langchain** for combining these components into a RAG pipeline
- **Streamlit** for the user interface

### Example Use Cases

- Analyze contracts and legal agreements
- Extract key terms and conditions from legal documents
- Find specific clauses or legal definitions in large documents
- Understand complex legal language by asking questions

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
