"""
Central config for ModernizeIQ.

One switch moves the whole app between your laptop (Ollama) and the AMD GPU (vLLM).
Set the environment variable USE_AMD=true to point at the AMD VM; leave it unset for local dev.

Both Ollama and vLLM expose an OpenAI-compatible API, so the only things that change
are the base_url and the model name. Nothing else in the codebase changes.
"""

import os

USE_AMD = os.getenv("USE_AMD", "false").lower() == "true"

if USE_AMD:
    # AMD Developer Cloud — vLLM serving Qwen2.5-7B-Instruct
    # Replace <vm-ip> with the VM's IP each session (or set AMD_BASE_URL env var)
    LLM_BASE_URL = os.getenv("AMD_BASE_URL", "http://<vm-ip>:8000/v1")
    LLM_MODEL = "Qwen/Qwen2.5-7B-Instruct"
    LLM_API_KEY = "EMPTY"
else:
    # Local dev — Ollama serving the same model family
    LLM_BASE_URL = "http://localhost:11434/v1"
    LLM_MODEL = "qwen2.5:7b"
    LLM_API_KEY = "ollama"  # Ollama ignores the value but the client needs a non-empty string

# Embeddings run locally via sentence-transformers (no GPU required, no external API)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Paths
DATA_PATH = "data/synthetic_apps.json"
KNOWLEDGE_BASE_DIR = "knowledge_base"
CHROMA_DIR = "chroma_db"
CHROMA_COLLECTION = "modernization_patterns"
