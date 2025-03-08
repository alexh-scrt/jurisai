# JurisAI Development Guidelines

## Build, Test, and Lint Commands
- Create conda environment: `conda create -n jurisai python=3.12`
- Activate environment: `conda activate jurisai`
- Install dev dependencies: `pip install -e ".[dev]"`
- Run all tests: `pytest`
- Run single test: `pytest tests/test_file.py::test_function -v`
- Code formatting: `black .` and `isort .`
- Type checking: `mypy src`
- Linting: `flake8 src`
- Run application: `./main.py` or `python -m src.jurisai`
- Launch web interface: `./main.py web` or `jurisai web`

## Code Style Guidelines
- **Formatting**: Black with 88 character line length, isort with black profile
- **Types**: Use type hints everywhere; enable strict mypy checking
- **Naming**: snake_case for variables/functions, PascalCase for classes
- **Imports**: Group imports (1.stdlib, 2.third-party, 3.local)
- **Package Imports**: Use absolute imports with `src.jurisai` prefix
- **Docstrings**: Google style docstrings for all public functions/classes
- **Error handling**: Use specific exceptions; document error cases
- **Data privacy**: Never log or expose PII or sensitive legal information
- **Testing**: Write tests for all new features; aim for >90% coverage
- **Logging**: Use structured logging with key-value pairs

## Technologies
- **Streamlit**: Used for web interface
- **Langchain**: Framework for building LLM applications
- **Hugging Face**: Used for embeddings models
- **FAISS**: Vector store for efficient similarity search
- **Ollama**: Local LLM server
- **Semantic Chunking**: Used for document splitting based on meaning
- **RAG (Retrieval Augmented Generation)**: Architecture for document Q&A

## LLM Requirements
For the web interface, you need to have Ollama installed and running:
1. Install Ollama: https://ollama.ai/
2. Pull the model: `ollama pull deepseek-r1:1.5b`
3. Alternatively, you can use other models like llama2, mistral, or gemma

Note: As this is a legal AI application, consider additional security measures for sensitive data.