
import json
from pathlib import Path

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Find the current app folder
BASE_DIR = Path(__file__).resolve().parent


# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Load saved policy chunks
POLICY_FILE = BASE_DIR / "policy_chunks.json"

with open(POLICY_FILE, "r", encoding="utf-8") as file:
    policy_chunks = json.load(file)


# Convert policy text into embeddings
policy_texts = [
    chunk["content"]
    for chunk in policy_chunks
]

policy_embeddings = model.encode(policy_texts)


def search_policies(question, top_k=3):
    # Convert user question into an embedding
    question_embedding = model.encode([question])

    # Calculate similarity
    similarities = cosine_similarity(
        question_embedding,
        policy_embeddings
    )[0]

    # Sort results by similarity
    ranked_indexes = similarities.argsort()[::-1]

    results = []

    for index in ranked_indexes[:top_k]:
        results.append({
            "filename": policy_chunks[index]["filename"],
            "content": policy_chunks[index]["content"],
            "score": float(similarities[index])
        })

    return results


if __name__ == "__main__":
    question = input("Ask a policy question: ")

    results = search_policies(question)

    print("\nRelevant Policies:\n")

    for result in results:
        print("File:", result["filename"])
        print("Similarity:", round(result["score"], 4))
        print("Content:", result["content"][:300])
        print("-" * 60)