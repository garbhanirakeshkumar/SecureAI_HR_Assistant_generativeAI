import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from .models import HRDocumentChunk


# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def search_policies(question, top_k=3):
    """
    Search only documents uploaded by HR.

    Built-in/project policy documents are NOT used.
    """

    # Get only HR-uploaded document chunks
    database_chunks = list(
        HRDocumentChunk.objects.select_related(
            "document"
        ).all()
    )

    # No HR documents uploaded yet
    if not database_chunks:
        return []

    # Create embedding for user's question
    question_embedding = model.encode(
        [question]
    )

    # Get stored document embeddings
    database_embeddings = np.array(
        [
            chunk.embedding
            for chunk in database_chunks
        ]
    )

    # Calculate similarity
    similarities = cosine_similarity(
        question_embedding,
        database_embeddings
    )[0]

    results = []

    for index, score in enumerate(similarities):

        chunk = database_chunks[index]

        results.append({
            "filename": chunk.document.title,
            "content": chunk.content,
            "score": float(score),
        })

    # Most relevant chunks first
    results.sort(
        key=lambda result: result["score"],
        reverse=True
    )

    return results[:top_k]