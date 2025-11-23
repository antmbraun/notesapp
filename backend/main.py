import os
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
import uvicorn
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from semantic_search import get_embedding, get_notes_by_description
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title="Notes App", description="A simple notes application with FastAPI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Note(BaseModel):
    title: str | None = None
    content: str
    summary: str | None = None
    description_embedding: list[float] | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)  # pyright: ignore[reportDeprecated]
    updated_at: datetime = Field(default_factory=datetime.utcnow)  # pyright: ignore[reportDeprecated]


# class NoteCreate(NoteBase):
#     pass

# Serially indexed list of notes, each one a dict with title, content
notes = []


def _try_summarize_notes(notes: list[Note]) -> None:
    """
    Call the summarize method on every note in the list of notes (method has side effect of
    saving the summary to the note if it doesn't already exist).
    """
    _ = (summarize(note) for note in notes)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Notes App</title>
        </head>
        <body>
            <h1>Welcome to Notes App</h1>
            <p>API Documentation: <a href="/docs">/docs</a></p>
            <p>Alternative docs: <a href="/redoc">/redoc</a></p>
        </body>
    </html>
    """


@app.get("/notes")
async def get_notes(description: str | None = None, top_k: int | None = None):
    """
    Returns a list of notes.
    If description is provided, returns notes sorted by similarity to the description using semantic similarity with a Hugging Face embedding model.
    If description is not provided, returns all notes.
    top_k limits the number of notes returned.
    """
    if description:
        result = get_notes_by_description(notes, description)
    else:
        result = notes

    result = result[:top_k]

    _try_summarize_notes(result)
    return result


@app.post("/notes")
async def create_note(note: Note):

    # Summarize the note
    try:
        summarize(note)
    except Exception as e:  # TODO: Handle error
        print(f"Error summarizing note: {e}")

    # Get the description embedding of the note
    try:
        note.description_embedding = get_embedding(note.content)
    except Exception as e:
        print(f"Error getting embedding: {e}")
        note.description_embedding = None

    notes.append(note)

    return {"message": "Note created", "note": note}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/summarize")
def summarize(req: Note):

    # Check if summary already was successfully generated
    if req.summary:
        return {"summary": req.summary}

    token = os.getenv("HF_TOKEN")
    if token is None:
        raise ValueError("HF_TOKEN is not set")

    client = InferenceClient(model="deepseek-ai/DeepSeek-V3-0324", token=token)

    # TODO: Double-check that chat.completions.create uses these parameters
    try:
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3-0324",
            messages=[
                {
                    "role": "user",
                    "content": f"{req.content}\n\nPlease summarize the above text in 50 words or less.",
                }
            ],
        )

        summary = completion.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

    # Save the summary to the note
    req.summary = summary

    return {"summary": summary}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
