from langchain_text_splitters import RecursiveCharacterTextSplitter

from .config import CHUNK_SIZE, CHUNK_OVERLAP


def split_documents(docs, mode: str = "recursive"):
    if mode == "semantic":
        from langchain_experimental.text_splitter import SemanticChunker
        from .embeddings import get_embeddings   # بيتكتب في خطوة ملك
        splitter = SemanticChunker(get_embeddings(), breakpoint_threshold_type="percentile")
    else:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""],
            add_start_index=True,
        )
    chunks = splitter.split_documents(docs)
    for i, c in enumerate(chunks):
        c.metadata["chunk_id"] = i
    return chunks


if __name__ == "__main__":
    from .ingest import load_documents
    docs = load_documents()
    chunks = split_documents(docs, "recursive")
    avg = sum(len(c.page_content) for c in chunks) / max(len(chunks), 1)
    print(f"recursive: {len(chunks)} chunks, avg {avg:.0f} chars")
    print(chunks[0].metadata)
    print(chunks[0].page_content[:300])