import numpy as np
import faiss
from google import genai


client = genai.Client()

EMBEDDING_MODEL = "gemini-embedding-2"


def create_embeddings(chunks):
    """Create embeddings for contract chunks."""

    embeddings = []

    for chunk in chunks:
        result = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=chunk["text"]
        )

        embeddings.append(result.embeddings[0].values)

    return np.array(embeddings, dtype="float32")


def create_faiss_index(embeddings):
    """Create FAISS similarity search index."""

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return index


def search_contract(question, chunks, index, top_k=3):
    """Find the most relevant contract sections."""

    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=question
    )

    question_embedding = np.array(
        [result.embeddings[0].values],
        dtype="float32"
    )

    distances, indices = index.search(question_embedding, top_k)

    results = []

    for distance, index_number in zip(distances[0], indices[0]):
        if index_number < len(chunks):
            results.append({
                "text": chunks[index_number]["text"],
                "page": chunks[index_number]["page"],
                "distance": float(distance)
            })

    return results