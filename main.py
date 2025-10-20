from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uvicorn

app = FastAPI(title="Notes App", description="A simple notes application with FastAPI")

# Pydantic models
class Note(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

# class NoteCreate(NoteBase):
#     pass

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
async def get_notes():
    return {"notes": notes}

@app.post("/notes")
async def create_note(note: dict):
    notes.append(note)
    return {"message": "Note created", "note": note}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
