# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

An MCP (Model Context Protocol) server exposing document-processing tools (currently document-to-markdown conversion, plus a demo `add` tool) to AI assistants like Claude. Built with `mcp[cli]` (FastMCP) and `markitdown`.

## Commands

```bash
# Setup (uv-managed venv)
uv venv
uv pip install -e .

# Run the MCP server (stdio transport; blocks waiting for a client)
uv run main.py

# Run all tests
uv run pytest

# Run a single test file / test
uv run pytest tests/test_document.py
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_pdf
```

### Windows / OneDrive environment notes

This repo path lives under OneDrive, which rejects `uv`'s default hardlink-based installs with `os error 396`. Set `UV_LINK_MODE=copy` (e.g. `export UV_LINK_MODE=copy`) before `uv venv` / `uv pip install` / `uv run` if you hit that error. Also check for a stale `VIRTUAL_ENV` env var left over from another project directory (`unset VIRTUAL_ENV`) if `uv` appears to install into the wrong `.venv`.

## Architecture

- `main.py` — the MCP server entrypoint. Creates a `FastMCP("docs")` instance and registers tool functions with `mcp.tool()(fn)`. **Defining a function in `tools/` does not expose it to the server** — it must be explicitly registered here.
- `tools/` — plain Python functions implementing tool logic, decoupled from MCP registration. Each function is registered individually in `main.py`, so the server's actual tool surface = whatever is wired up in `main.py`, not everything present in `tools/`.
  - `tools/document.py` — `binary_document_to_markdown(binary_data, file_type)` wraps `markitdown.MarkItDown` to convert binary document bytes (docx, pdf, etc.) into markdown text via a `BytesIO`/`StreamInfo` stream.
  - `tools/math.py` — `add(a, b)` — trivial demo tool.
- `tests/` — pytest tests import directly from `tools.*` (not through the MCP layer), with binary fixtures in `tests/fixtures/` (`mcp_docs.docx`, `mcp_docs.pdf`).

## Defining new MCP tools

Per `README.md`, tool functions follow this pattern:

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does")
) -> ReturnType:
    """Comprehensive docstring here"""
    # Implementation
```

Then register it in `main.py`:

```python
mcp.tool()(my_function)
```

Tool docstrings should:
- Begin with a one-line summary
- Provide a detailed explanation of functionality
- Explain when to use (and not use) the tool
- Include usage examples with expected input/output (see `tools/math.py:add` for the reference example, including doctest-style `>>>` examples)

Every parameter should use `Field(description=...)` from pydantic rather than a bare type annotation — the description is what the calling assistant sees when deciding how to call the tool.

## Code style

Always give function arguments (and return values) appropriate type annotations — no untyped/bare parameters, in tool functions or elsewhere in this codebase.
