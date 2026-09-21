# Building with the Claude API

Hands-on work through Anthropic's [Building with the Claude API](https://academy.claude.com/courses/building-with-the-claude-api) course. Six modules of runnable notebooks and projects covering the API, prompt evals, tool use, MCP, RAG and Claude Code, all running against current Claude models.

## How I worked through it

The course is code-along: lessons come with starter code and guided walkthroughs. I ran every lesson end to end, completed the exercises and open TODOs, and updated the material for current models and SDK behaviour rather than copying the videos verbatim. In practice that meant:

- Moving to `claude-sonnet-5` (and `claude-haiku-4-5` for the RAG helpers), which surfaced two API changes worth knowing: `effort` replaces `temperature`, and assistant prefill is no longer accepted.
- Making helpers more robust, for example finding the text block in a response instead of assuming `content[0]`, and stripping code fences defensively in the eval graders.
- Choosing the text editor tool schema based on the model in use.
- Batching embedding calls with a bulk `add_documents` so the RAG notebooks stay under Voyage AI rate limits.
- Setting up Claude Code properly for module 06, with a `CLAUDE.md` and custom worktree commands.

Course content and starter code belong to Anthropic; this repo is unofficial.

## What's covered

| Folder | Topic | Course sections | Format |
| --- | --- | --- | --- |
| [`01-api-basics`](01-api-basics) | Requests, system prompts, effort, streaming, stop sequences | Accessing Claude with the API | Notebooks |
| [`02-prompt-evaluation`](02-prompt-evaluation) | Building eval pipelines and prompt engineering | Prompt Evaluation, Prompt Engineering Techniques | Notebooks |
| [`03-tool-use`](03-tool-use) | Tool use plus Claude's built-in features | Tool Use with Claude, Features of Claude | Notebooks |
| [`04-mcp`](04-mcp) | MCP server and client | Model Context Protocol | Python project |
| [`05-rag`](05-rag) | Retrieval pipeline from chunking to contextual retrieval | RAG and Agentic Search | Notebooks |
| [`06-claude-code`](06-claude-code) | Claude Code workflow on a small MCP server | Anthropic Apps: Claude Code | Python project |

The course's Agents and Workflows section (parallelization, chaining, routing) is not in this repo.

## Module notes

### 01 - API basics

Five notebooks that build up a small chat helper: a basic request and multi-turn message history (`001`), system prompts (`002`), temperature (`003`), streaming with `stream=True` and the SDK's stream helper (`004`), and controlling output with stop sequences (`005`).

Two things differ from the course videos because the notebooks target a newer model. `temperature` is no longer supported and is replaced by `effort`, which controls how much the model reasons rather than how varied the wording is. Assistant message prefilling is also no longer accepted (it returns a 400), so `005` documents that and points to system-prompt instructions as the replacement.

### 02 - Prompt evaluation

- `001_prompt_evals.ipynb` follows the course's step-by-step eval loop: generate a test dataset with Claude, run a prompt over it, then grade each output with both code-based checks (valid JSON, Python and regex) and model-based grading against per-case criteria.
- `002_prompting.ipynb` uses the course's reusable `PromptEvaluator` class to test a prompt end to end. The example task is a one-day meal plan for an athlete, with three generated test cases in `dataset.json` (weightlifter, swimmer, vegetarian marathon runner).
- `output.json` and `output.html` are the raw results and the HTML report from that run.

### 03 - Tool use and Claude features

| Notebook | Topic |
| --- | --- |
| `001_tools` | Tool schemas and functions (`get_current_datetime`, `add_duration_to_datetime`, `set_reminder`) |
| `002_multi_turn` | Multi-turn tool loop, running several tools per response |
| `003_structured_data` | Structured output via a tool schema and `tool_choice` |
| `004 _tool_streaming` | Streaming tool calls, including fine-grained tool input |
| `005_text_editor_tool` | A local `TextEditorTool` implementation with path validation and backups |
| `006_web_search` | Server-side web search tool |
| `007_thinking` | Extended thinking, including redacted thinking |
| `008_images` | Image input (property photos in `images/`), PDF input (`earth.pdf`) and citations |
| `009_caching` | Prompt caching with a large system prompt and tool schemas |
| `010_code_execution` | Code execution tool and the Files API (`streaming.csv`, `churn_driver_analysis.png`) |

`main.py`, `test.py` and `.backups/` are files produced by the text editor exercise (a `calculate_pi` function, its unit tests, and the tool's automatic backups).

### 04 - Model Context Protocol

A command-line chat app that connects Claude to an MCP server. The scaffold (`core/`, `main.py`, the CLI and the module README) is the course's starter project; the MCP pieces were filled in during the lessons:

- `mcp_server.py` exposes two tools (`read_doc_contents`, `edit_document`), two resources (`docs://documents` and `docs://documents/{doc_id}`) and one prompt (`format`) over an in-memory set of documents.
- `mcp_client.py` is an async `MCPClient` that wraps the stdio connection and provides `list_tools`, `call_tool`, `list_prompts`, `get_prompt` and `read_resource`.

The `summarize` prompt is left as a TODO in the server, so `/summarize` from the module's own README is not implemented. Only `/format` works.

### 05 - RAG

The pipeline is built up one notebook at a time, all against `report.md` (a synthetic company annual report supplied by the course as the corpus):

1. `001_chunking` - by character, by sentence and by section
2. `002_embeddings` - embeddings with Voyage AI (`voyage-3-large`)
3. `003_vectordb` - a `VectorIndex` class with cosine search
4. `004_bm25` - a `BM25Index` class for lexical search
5. `005_hybrid` - a `Retriever` that merges vector and BM25 results with reciprocal rank fusion
6. `006_reranking` - a Claude-based reranker over the merged results
7. `007_contextual_retrieval` - Claude adds a short situating context to each chunk before indexing

### 06 - Claude Code

A small MCP server ("docs") used as the practice project for the Claude Code lessons, with Claude Code doing most of the editing. It registers two tools: `add` and `document_path_to_markdown`, which converts PDF and DOCX files to Markdown with [markitdown](https://github.com/microsoft/markitdown). Tests in `tests/` use PDF and DOCX fixtures.

The Claude Code setup itself is part of the repo: `CLAUDE.md` documents the project for the assistant, and `.claude/commands/` holds two custom slash commands, `create_worktree` and `merge_worktree`.

## Getting started

Requires Python 3.10+ and an [Anthropic API key](https://console.anthropic.com/).

```bash
git clone https://github.com/yazanlouid/claude-api-course.git
cd claude-api-course
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                 # then fill in your keys
python test_claude.py                                # quick check that your key works
jupyter notebook                                     # open any notebook in 01, 02, 03 or 05
```

`.env` variables:

| Variable | Needed for |
| --- | --- |
| `ANTHROPIC_API_KEY` | Everything |
| `VOYAGE_API_KEY` | Module 05 (embeddings) |
| `CLAUDE_MODEL` | Module 04 CLI (`main.py` refuses to start without it) |

Notebooks set the model in a `model = "..."` line near the top (most use `claude-sonnet-5`, the RAG notebooks use `claude-haiku-4-5`), so swap it if you want a different one. Module 05 installs `voyageai` from inside its notebooks.

### Running the projects

Modules 04 and 06 are standalone [uv](https://docs.astral.sh/uv/) projects with their own `pyproject.toml`:

```bash
cd 04-mcp
uv venv && source .venv/bin/activate
uv pip install -e .
uv run main.py            # chat CLI; use @doc_id to attach a document, /format doc_id to run the prompt
```

```bash
cd 06-claude-code
uv venv && source .venv/bin/activate
uv pip install -e .
uv run main.py            # starts the MCP server over stdio
uv run pytest             # runs the tests
```

Set `USE_UV=1` in `.env` if you want module 04 to launch its server through `uv run` instead of `python`.

## Repo layout

```
.
├── 01-api-basics/          notebooks 001-005
├── 02-prompt-evaluation/   notebooks, dataset.json, output.json, output.html
├── 03-tool-use/            notebooks 001-010, sample images/PDF/CSV, text editor outputs
├── 04-mcp/                 MCP chat app: server, client, core/ CLI
├── 05-rag/                 notebooks 001-007, report.md corpus
├── 06-claude-code/         docs MCP server, tests, CLAUDE.md, .claude/commands
├── .env.example
├── requirements.txt        anthropic, python-dotenv, jupyter
└── test_claude.py          minimal API smoke test
```
