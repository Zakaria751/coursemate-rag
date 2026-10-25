import re
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader

from .config import DATA_DIR


def clean_text(text: str) -> str:
    text = re.sub(r"-\n(\w)", r"\1", text)      # كلمات اتقسمت بين سطرين
    text = re.sub(r"[ \t]+", " ", text)          # مسافات زيادة
    text = re.sub(r"\n{3,}", "\n\n", text)       # أسطر فاضية كتير
    return text.strip()


def load_documents(data_dir: Path = DATA_DIR):
    docs = []
    for path in sorted(Path(data_dir).rglob("*")):
        ext = path.suffix.lower()
        if ext == ".pdf":
            loader = PyPDFLoader(str(path))
        elif ext in (".txt", ".md"):
            loader = TextLoader(str(path), encoding="utf-8")
        else:
            continue
        try:
            loaded = loader.load()
        except Exception as e:
            print(f"[SKIP] {path.name}: {e}")
            continue

        for d in loaded:
            d.page_content = clean_text(d.page_content)
            d.metadata["source"] = path.name
            d.metadata["course"] = path.parent.name
            page = d.metadata.get("page")
            d.metadata["page_display"] = (page + 1) if isinstance(page, int) else 1
        docs.extend(d for d in loaded if len(d.page_content) > 50)
        print(f"[OK] {path.name}: {len(loaded)} page(s)")
    return docs


if __name__ == "__main__":
    documents = load_documents()
    print(f"\nTotal: {len(documents)} pages/documents")
    if documents:
        print(documents[0].metadata)
        print(documents[0].page_content[:300])