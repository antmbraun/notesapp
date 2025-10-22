import os

from fastapi.testclient import TestClient
from main import app
from unittest.mock import MagicMock, patch
from types import SimpleNamespace

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_notes_empty():
    response = client.get("/notes")
    assert response.status_code == 200


def test_create_note():
    response = client.post(
        "/notes", json={"title": "Test Note", "content": "Test content"}
    )
    assert response.status_code == 200
    assert "note" in response.json()


def test_get_notes_after_create():
    # Create a note
    client.post("/notes", json={"title": "Note 1", "content": "Content 1"})

    # Get all notes
    response = client.get("/notes")
    assert response.status_code == 200
    data = response.json()
    assert "notes" in data


def test_summarize_success():
    # Fake completion object with the nested shape your code reads
    # These are safeguards to ensure the LLM is called correctly, especially
    # that there are not too many calls to the LLM.
    if os.getenv("HF_TOKEN") is None:
        raise ValueError("HF_TOKEN is not set")

    completion = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="Mock summary"))]
    )

    fake_client = MagicMock()
    fake_client.chat.completions.create.return_value = completion

    with patch("main.InferenceClient", return_value=fake_client) as mock_cls:
        resp = client.post(
            "/summarize", json={"text": "This is a long text to summarize."}
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["summary"] == "Mock summary"
        mock_cls.assert_called_once()
        fake_client.chat.completions.create.assert_called_once()


def test_summarize_error():
    # This test ensures that the server can handle errors from the LLM gracefully.
    fake_client = MagicMock()
    fake_client.chat.completions.create.side_effect = Exception("Boom")

    with patch("main.InferenceClient", return_value=fake_client):
        resp = client.post("/summarize", json={"text": "Trigger error"})
        assert resp.status_code == 502
        assert "Boom" in resp.json()["detail"]


# This test will actually call the LLM. It is not a mock test, and will fail
# if the Hugging Face API is not available.
def test_summarize_live_user_string():
    # Prefer external file; fallback to the dummy string
    text = "TEST STRING"
    try:
        with open("test_string.txt", "r", encoding="utf-8") as f:
            contents = f.read().strip()
            if contents:
                text = contents
    except FileNotFoundError:
        pass

    payload = {"text": text}

    resp = client.post("/summarize", json=payload)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert "summary" in data
    assert isinstance(data["summary"], str) and len(data["summary"]) > 0

    # For developer human checking - need to call pytest with -s to see the output
    print(data["summary"])
