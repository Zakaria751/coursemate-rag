import shutil

from langchain_chroma import Chroma

from .config import CHROMA_DIR, COLLECTION_NAME
from .embeddings import get_embeddings


def _open_store():
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=str(CHROMA_DIR),
        collection_metadata={"hnsw:space": "cosine"},
    )


def build_index(chunks, reset: bool = True):
    if reset and CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)
    vs = _open_store()
    batch = 100
    for i in range(0, len(chunks), batch):
        part = chunks[i:i + batch]
        vs.add_documents(part, ids=[f"chunk-{c.metadata['chunk_id']}" for c in part])
        print(f"Indexed {min(i + batch, len(chunks))}/{len(chunks)}")
    return vs


def load_vectorstore():
    return _open_store()