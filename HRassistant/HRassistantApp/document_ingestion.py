from sentence_transformers import SentenceTransformer

from .models import HRDocumentChunk


# Load embedding model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def create_chunks(text, chunk_size=500, overlap=100):
    """
    Split document text into overlapping chunks.
    """

    text = text.strip()

    if not text:
        return []

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def process_document(document, text):
    """
    Create chunks and embeddings for an HRDocument.
    """

    chunks = create_chunks(text)

    if not chunks:
        return 0

    embeddings = embedding_model.encode(chunks)

    created_count = 0

    for chunk_text, embedding in zip(chunks, embeddings):

        HRDocumentChunk.objects.create(
            document=document,
            content=chunk_text,
            embedding=embedding.tolist()
        )

        created_count += 1

    return created_count