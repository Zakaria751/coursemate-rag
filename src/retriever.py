from .config import TOP_K
from .vectorstore import load_vectorstore


def get_retriever(k: int = TOP_K, mode: str = "similarity", course: str | None = None):
    """mode: 'similarity' أو 'mmr' (بيقلل التكرار بين النتايج)."""
    vs = load_vectorstore()
    kwargs = {"k": k}
    if mode == "mmr":
        kwargs.update(fetch_k=20, lambda_mult=0.5)
    if course:
        kwargs["filter"] = {"course": course}
    return vs.as_retriever(search_type=mode, search_kwargs=kwargs)


def search_with_scores(query: str, k: int = TOP_K, course: str | None = None):
    """بترجع (Document, distance). الأصغر = الأقرب."""
    vs = load_vectorstore()
    flt = {"course": course} if course else None
    return vs.similarity_search_with_score(query, k=k, filter=flt)


if __name__ == "__main__":
    q = input("Query: ")
    for doc, dist in search_with_scores(q):
        print(f"\n--- distance={dist:.3f} | {doc.metadata['source']} p.{doc.metadata['page_display']}")
        print(doc.page_content[:300])