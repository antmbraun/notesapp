import os
from datetime import datetime

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

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


class SummaryRequest(BaseModel):
    text: str
    model: str = "deepseek-ai/DeepSeek-V3-0324"
    min_length: int | None = 30
    max_length: int | None = 130
    do_sample: bool = False
    endpoint_url: str | None = None


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


@app.post("/summarize")
def summarize(req: SummaryRequest):
    token = os.getenv("HF_TOKEN")

    client = (
        InferenceClient(endpoint=req.endpoint_url, token=token)
        if req.endpoint_url
        else InferenceClient(model=req.model, token=token)
    )

    # TODO: Double-check that chat.completions.create uses these parameters
    params = {
        k: v
        for k, v in {
            "min_length": req.min_length,
            "max_length": req.max_length,
            "do_sample": req.do_sample,
        }.items()
        if v is not None
    }

    try:
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3-0324",
            messages=[
                {
                    "role": "user",
                    "content": f"{req.text}\n\nPlease summarize the above text in 50 words or less.",
                }
            ],
        )

        summary = completion.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

    return {
        "summary": summary,
        "model": req.model,
        "endpoint": req.endpoint_url or "hub",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
