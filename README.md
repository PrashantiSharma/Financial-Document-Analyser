# Financial Document Analyzer

A lightweight FastAPI application that inspects PDF reports with a small
deterministic language model.  The service exposes a simple API for uploading
financial documents and receiving high‑level analysis.

## Bugs and Fixes

| Original issue | Resolution |
| --- | --- |
| Agents used unsafe, vague prompts and referenced an undefined LLM | Replaced with clear professional prompts and a local `DummyLLM` stub for deterministic behaviour |
| PDF tool relied on an unavailable library and static paths | Rebuilt using `pypdf`, added path validation and hooked the API upload path into the workflow |
| API entry point left temporary files behind and produced weak error messages | Added robust file handling, error propagation and cleanup |

## Setup

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the test suite**

   ```bash
   pytest -q
   ```

## Usage

Start the API with Uvicorn:

```bash
uvicorn main:app --reload
```

### Endpoints

| Method & Path | Description |
| --- | --- |
| `GET /` | Health check returning a status message |
| `POST /analyze` | Upload a PDF (`file`) and optional `query` to receive an analysis |

Example using `curl`:

```bash
curl -X POST -F "file=@data/TSLA-Q2-2025-Update.pdf" \
     -F "query=Summarise key risks" \
     http://localhost:8000/analyze
```

## Project Structure

* `agents.py` – defines analysis agents powered by a deterministic LLM stub
* `tools.py` – PDF reading and web search helpers
* `task.py` – CrewAI tasks that orchestrate agent behaviour
* `main.py` – FastAPI entry point and crew execution wiring

## Development Notes

The repository includes a sample Tesla earnings report at
`data/TSLA-Q2-2025-Update.pdf`.  When the API receives a document upload it
temporarily stores the file and removes it after processing.

