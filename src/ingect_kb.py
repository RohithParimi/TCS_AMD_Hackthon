"""
Ingest the knowledge base into ChromaDB.

Reads every markdown file in knowledge_base/, embeds it with a local
sentence-transformers model, and stores it in a persistent ChromaDB collection.
The decision agent retrieves from this collection at analysis time.

Run once (re-run any time you change the knowledge base):
    uv run src/ingest_kb.py
"""

import os
import sys
import glob
import chromadb
from chromadb.utils import embedding_functions

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import KNOWLEDGE_BASE_DIR, CHROMA_DIR, CHROMA_COLLECTION, EMBEDDING_MODEL  # noqa: E402


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    kb_dir = os.path.join(root, KNOWLEDGE_BASE_DIR)
    files = sorted(glob.glob(os.path.join(kb_dir, "*.md")))

    if not files:
        print(f"No .md files found in {kb_dir}. Nothing to ingest.")
        return

    # Local embedding model — downloads ~80MB once, then cached. No GPU, no API.
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)

    client = chromadb.PersistentClient(path=os.path.join(root, CHROMA_DIR))

    # Reset the collection so re-ingesting is idempotent
    try:
        client.delete_collection(CHROMA_COLLECTION)
    except Exception:
        pass
    col = client.create_collection(CHROMA_COLLECTION, embedding_function=ef)

    docs, ids, metas = [], [], []
    for path in files:
        with open(path, encoding="utf-8") as f:
            docs.append(f.read())
        name = os.path.basename(path)
        ids.append(name)
        metas.append({"source": name})

    col.add(documents=docs, ids=ids, metadatas=metas)
    print(f"Ingested {len(docs)} knowledge base documents into '{CHROMA_COLLECTION}'.")
    print("Sources:")
    for name in ids:
        print(f"  - {name}")


if __name__ == "__main__":
    main()