# ModernizeIQ — Local Workstation Setup

Goal: a laptop dev environment that mirrors the AMD GPU exactly, so you build here
(off the GPU clock) and only use AMD windows for validation, metrics, and the demo recording.

The model serving differs by machine, but both speak the OpenAI API:
- **Local:** Ollama serving `qwen2.5:7b`
- **AMD:**   vLLM serving `Qwen/Qwen2.5-7B-Instruct`

`config.py` switches between them with one env var. Nothing else changes.

---

## 1. Install Ollama (the local model server)

Windows: download and run the installer from https://ollama.com/download
Then, in a terminal:

```
ollama pull qwen2.5:7b
```

Ollama runs a background server on http://localhost:11434 with an OpenAI-compatible
endpoint at /v1. Leave it running.

## 2. Install uv (the Python env manager)

Windows PowerShell:

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

(Restart the terminal afterwards so `uv` is on PATH.)

## 3. Create the environment and run the smoke test

From the repo root:

```
uv venv
uv pip install openai
uv run smoke_test.py
```

You should see a coherent sentence about the 6R framework and a token count.
That confirms your local model path works and mirrors AMD.

## 4. Install the rest of the dependencies (for the build)

```
uv pip install -r requirements.txt
```

(crewai is large; this can take a few minutes.)

## 5. Lock the environment for the AMD VM

After everything installs, freeze it so the VM gets an identical environment:

```
uv pip freeze > requirements.lock.txt
```

On the AMD VM later: `uv venv && uv pip install -r requirements.lock.txt`

---

## Switching to AMD (later, for validation/metrics/demo)

On the AMD VM, start vLLM (model is already cached in your snapshot):

```
vllm serve Qwen/Qwen2.5-7B-Instruct --port 8000 --max-model-len 8192
```

Then run the app with:

```
USE_AMD=true AMD_BASE_URL=http://localhost:8000/v1 uv run smoke_test.py
```

Same code, AMD inference.

---

## What's already in this repo

- `data/synthetic_apps.json` — 10 enterprise apps, one per 6R decision, from real seed data
- `knowledge_base/` — 15 modernization pattern / anti-pattern / gotcha / rationale docs for RAG
- `config.py` — the local↔AMD switch
- `smoke_test.py` — proves the model path works
- `src/` — agents, RAG ingestion, API, dashboard (built next)
