# Arabic Legal Document Q&A (RAG)

A RAG service that answers questions about the Egyptian Civil Code (Law of 1948). The source is a bilingual Arabic/English PDF. Every answer cites the source articles by article number.

## Setup

```bash
uv venv --python 3.12
uv pip install -e ".[dev]"
pre-commit install
pytest
```

If your shell sets `PYTHONPATH` (for example, ROS), run `env -u PYTHONPATH pytest`. Otherwise pytest loads foreign plugins.
