from langchain_huggingface import HuggingFaceEmbeddings

from .config import EMBEDDING_MODEL

_embeddings = None


def get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            encode_kwargs={"normalize_embeddings": True},
        )
    return _embeddings


if __name__ == "__main__":
    v = get_embeddings().embed_query("What is a Python list?")
    print(f"Vector dimension: {len(v)}")
    print(v[:5])