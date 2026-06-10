"""
Retrieval layer for ModernizeIQ.

Wraps the ChromaDB collection built by ingest_kb.py. The pipeline calls
retrieve_patterns() with a profile of the application, and gets back the most
relevant modernization patterns to ground the 6R decision.

We retrieve manually and inject the results into the decision agent's prompt,
rather than using agent tool-calling — local 7B models are unreliable at deciding
to call tools, but excellent at reasoning over context we hand them.
"""

import os
import sys
import chromadb
from chromadb.utils import embedding_functions

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CHROMA_DIR, CHROMA_COLLECTION, EMBEDDING_MODEL  # noqa: E402

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
_client = chromadb.PersistentClient(path=os.path.join(_root, CHROMA_DIR))


def _get_collection():
    try:
        return _client.get_collection(CHROMA_COLLECTION, embedding_function=_ef)
    except Exception as e:
        raise RuntimeError(
            f"Knowledge base collection '{CHROMA_COLLECTION}' not found. "
            f"Run `uv run src/ingest_kb.py` first."
        ) from e


def retrieve_patterns(query: str, k: int = 3) -> list[tuple[str, str]]:
    """Return the top-k (source_filename, document_text) most relevant to the query."""
    col = _get_collection()
    res = col.query(query_texts=[query], n_results=k)
    docs = res["documents"][0]
    sources = [m["source"] for m in res["metadatas"][0]]
    return list(zip(sources, docs))


if __name__ == "__main__":
    # Quick manual test
    q = "Java 7 legacy monolith on end-of-life RHEL 6, 11 CVEs, redundant, no roadmap"
    for src, doc in retrieve_patterns(q, k=3):
        print(f"\n=== {src} ===")
        print(doc[:200], "...")