
from policy_reader import read_policy_documents
import json


def split_into_chunks(
    text,
    chunk_size=500,
    overlap=100
):
    """
    Split text into overlapping word-based chunks.

    chunk_size: Maximum words per chunk.
    overlap: Number of words shared between chunks.
    """

    if overlap >= chunk_size:
        raise ValueError(
            "Overlap must be smaller than chunk size."
        )

    words = text.split()

    if not words:
        return []

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size

        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        if end >= len(words):
            break

        start = end - overlap

    return chunks


def create_policy_chunks():
    documents = read_policy_documents()
    all_chunks = []

    for document in documents:
        filename = document["filename"]

        # Skip non-policy files
        if filename.lower() == "readme.md":
            continue

        text = document["content"]

        chunks = split_into_chunks(
            text,
            chunk_size=500,
            overlap=100
        )

        for index, chunk in enumerate(chunks, start=1):
            all_chunks.append({
                "chunk_id": f"{filename}_{index}",
                "filename": filename,
                "chunk_number": index,
                "content": chunk
            })

    return all_chunks


if __name__ == "__main__":
    policy_chunks = create_policy_chunks()

    output_file = "policy_chunks.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(
            policy_chunks,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("Total policy chunks:", len(policy_chunks))
    print(f"Saved chunks to {output_file}")