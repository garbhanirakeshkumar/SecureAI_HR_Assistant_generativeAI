
from pathlib import Path

# Get the folder containing this file
BASE_DIR = Path(__file__).resolve().parent

# Location of policy documents
DOCUMENTS_DIR = BASE_DIR / "documents"


def read_policy_documents():
    policies = []

    for file_path in DOCUMENTS_DIR.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")

        policies.append({
            "filename": file_path.name,
            "content": content
        })

    return policies


if __name__ == "__main__":
    documents = read_policy_documents()

    print(f"Total documents: {len(documents)}")

    for document in documents:
        print("\nFile:", document["filename"])
        print(document["content"][:200])