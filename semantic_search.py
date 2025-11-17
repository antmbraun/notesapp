import os
from fastapi import HTTPException
from huggingface_hub import InferenceClient
from sklearn.metrics.pairwise import cosine_similarity


def get_notes_by_description(notes: list[dict], description: str, top_k: int | None = None):
    """
    Search notes using semantic similarity with a Hugging Face embedding model.
    
    Args:
        notes: List of notes to search through, each one a dict with title, content
        description: Natural language description of desired notes
        top_k: Number of top matching notes to return
    
    Returns:
        List of notes sorted by relevance
    """
    try:
        # Get embedding for the search description
        print(len(notes))
        description_embedding = get_embedding(description)
        
        # Get embeddings for all notes and compute similarity
        note_scores = []
        for note in notes:
            # Combine title and content for better matching
            note_text = f"{note.title or ''} {note.content or ''}"
            note_embedding = get_embedding(note_text)
            

            # print(f"len(note_embedding): {len(note_embedding)}")
            # print(f"len(description_embedding): {len(description_embedding)}")
            # Compute cosine similarity
            similarity = cosine_similarity(
                [description_embedding],
                [note_embedding]
            )[0][0]

            # Debug: print similarity
            # print(f"Similarity: {similarity}")
            
            note_scores.append((note, similarity))
        
        # Sort by similarity (highest first) and return top_k
        note_scores.sort(key=lambda x: x[1], reverse=True)
        return [note for note, _ in note_scores[:top_k]]
        
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=502, detail=f"Search failed: {str(e)}")

def get_embedding(text: str) -> list[float]:
    """
    Get embedding vector for text using Hugging Face Inference API.
    """
    token = os.getenv("HF_TOKEN")
    if token is None:
        raise HTTPException(status_code=500, detail="HF_TOKEN is not set")

    client = InferenceClient(model="sentence-transformers/all-MiniLM-L6-v2", token=token)

    try:
        response = client.feature_extraction(text)
        # feature_extraction returns a list of embeddings (one per input)
        # For a single input, extract the first embedding
        if isinstance(response, list) and len(response) > 0 and isinstance(response[0], list):
            return response[0]
        return response
    
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to get embedding: {str(e)}")