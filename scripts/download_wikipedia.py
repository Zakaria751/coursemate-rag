import time
from pathlib import Path

import requests

OUT = Path(__file__).resolve().parent.parent / "data" / "raw"
HEADERS = {"User-Agent": "CourseMateStudentProject/1.0 (university assignment)"}

TOPICS = {
    "programming": [
        "Python (programming language)", "Variable (computer science)", "Data type",
        "Control flow", "Conditional (computer programming)", "Loop (computer programming)",
        "Function (computer programming)", "Algorithm", "Sorting algorithm",
        "Binary search algorithm", "Big O notation", "Recursion (computer science)",
        "Data structure", "Array (data structure)", "Linked list",
        "Stack (abstract data type)", "Queue (abstract data type)", "Hash table",
        "Tree (data structure)", "Object-oriented programming", "Debugging",
        "Integrated development environment",
    ],
    "computers_society": [
        "Computer ethics", "Digital divide", "Information privacy", "Artificial intelligence",
        "Algorithmic bias", "Open-source software", "Software license", "Cybercrime",
        "Computer security", "Social media", "Technological unemployment",
    ],
}


def fetch(title: str, retries: int = 4) -> str:
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(
                "https://en.wikipedia.org/w/api.php",
                params={"action": "query", "prop": "extracts", "explaintext": 1,
                        "redirects": 1, "titles": title, "format": "json"},
                headers=HEADERS, timeout=30,
            )
            r.raise_for_status()
            page = next(iter(r.json()["query"]["pages"].values()))
            return page.get("extract", "")
        except Exception as e:
            wait = 5 * attempt
            print(f"   [retry {attempt}/{retries}] {title}: {e} (waiting {wait}s)")
            time.sleep(wait)
    return ""


if __name__ == "__main__":
    failed = []
    for course, titles in TOPICS.items():
        folder = OUT / course
        folder.mkdir(parents=True, exist_ok=True)
        for t in titles:
            name = "wiki_" + "".join(c if c.isalnum() else "_" for c in t.lower()).strip("_") + ".txt"
            if (folder / name).exists():
                print(f"[EXISTS] {name}")
                continue
            text = fetch(t)
            if len(text) < 500:
                print(f"[SKIP] {t} (too short, missing, or failed)")
                failed.append(t)
                continue
            (folder / name).write_text(f"{t}\n\n{text}", encoding="utf-8")
            print(f"[OK] {name} ({len(text)} chars)")
            time.sleep(2)
    print(f"\nDone. Skipped/failed: {failed}")