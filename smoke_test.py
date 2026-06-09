"""
Smoke test — proves your local model path works, identical to the AMD notebook test.

Run this AFTER:
  1. Ollama is installed and running
  2. You have pulled the model:  ollama pull qwen2.5:7b

Usage:
  uv run smoke_test.py

If this prints a coherent sentence, your laptop now mirrors the AMD GPU setup.
The same file, with USE_AMD=true, will hit the AMD VM instead — no code change.
"""

from openai import OpenAI
from config import LLM_BASE_URL, LLM_MODEL, LLM_API_KEY

client = OpenAI(base_url=LLM_BASE_URL, api_key=LLM_API_KEY)

resp = client.chat.completions.create(
    model=LLM_MODEL,
    messages=[
        {"role": "user", "content": "In one sentence, what is the 6R framework in application modernization?"}
    ],
    temperature=0.2,
)

print("BASE_URL:", LLM_BASE_URL)
print("MODEL:   ", LLM_MODEL)
print("-" * 60)
print(resp.choices[0].message.content)
print("-" * 60)
print("tokens used:", resp.usage.total_tokens)
print("\nIf you see a sentence above, your local workstation is ready.")
