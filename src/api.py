"""
ModernizeIQ API — thin FastAPI layer over the pipeline outputs.

Serves the precomputed portfolio (data/results.json from run_all.py) and offers a
live single-app analysis endpoint for the "watch the agents think" demo moment.

Run:
    uv run uvicorn src.api:app --reload --port 8080

Endpoints:
    GET  /portfolio          -> full precomputed results (meta + all apps)
    GET  /apps               -> the raw input applications
    POST /analyze/{app_id}   -> run the live 3-agent pipeline on one app (slow; demo use)
    GET  /health             -> liveness + which model/config is active
"""

import os
import sys
import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATA_PATH, LLM_MODEL, LLM_BASE_URL  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_PATH = os.path.join(ROOT, "data", "results.json")

app = FastAPI(title="ModernizeIQ API", version="1.0")

# Allow the Streamlit dashboard (and the static HTML mock) to call us from the browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _load_apps() -> list[dict]:
    with open(os.path.join(ROOT, DATA_PATH)) as f:
        return json.load(f)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": LLM_MODEL,
        "llm_base_url": LLM_BASE_URL,
        "results_available": os.path.exists(RESULTS_PATH),
    }


@app.get("/apps")
def get_apps():
    return _load_apps()


@app.get("/portfolio")
def get_portfolio():
    if not os.path.exists(RESULTS_PATH):
        raise HTTPException(
            status_code=404,
            detail="No results yet. Run `uv run src/run_all.py` to generate data/results.json.",
        )
    with open(RESULTS_PATH) as f:
        return json.load(f)


@app.post("/analyze/{app_id}")
def analyze_one(app_id: str):
    """Live pipeline run on a single app — the demo's 'watch it think' moment."""
    apps = _load_apps()
    target = next((a for a in apps if a["id"] == app_id), None)
    if target is None:
        raise HTTPException(status_code=404, detail=f"Unknown app_id: {app_id}")

    # Import here so the API starts fast and only loads the crew when needed
    from crew import analyze_app
    try:
        return analyze_app(target)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {e}")