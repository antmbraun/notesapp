import os
from datetime import datetime

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from cache import cache_summary, get_cached_summary
from semantic_search import get_notes_by_description

load_dotenv()

app = FastAPI(title="Notes App", description="A simple notes application with FastAPI")


# Pydantic models
class Note(BaseModel):
    title: str | None = None
    content: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


# class NoteCreate(NoteBase):
#     pass

# Serially indexed list of notes, each one a dict with title, content
notes = []

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
async def get_notes(description: str | None = None, top_k: int | None = 5):
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

    """
    Cast Note objects to dicts because we need to add a summary field.
    Include summaries for each note in the list.
    """
    result2 = []
    for note in result:
        temp = note.model_dump()
        temp["summary"] = summarize(note).get("summary")
        result2.append(temp)
    
    return result2


@app.post("/notes")
async def create_note(note: Note):
    notes.append(note)

    # Summarize the note
    try:
        summarize(note)
    except Exception as e:  # TODO: Handle error
        print(f"Error summarizing note: {e}")

    return {"message": "Note created", "note": note}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/summarize")
def summarize(req: Note):

    # Check for cached summary
    cached_summary = get_cached_summary(req.content)
    if cached_summary is not None:
        return {"summary": cached_summary}
    
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

    # Cache the summary
    cache_summary(req.content, summary)

    return {"summary": summary}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
