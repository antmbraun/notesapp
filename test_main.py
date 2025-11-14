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
    assert "Note" in data[0]["title"]


def test_summarize_success():
    # Fake completion object with the nested shape your code reads
    # These are safeguards to ensure the LLM is called correctly, especially
    # that there are not too many calls to the LLM.

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

    if os.getenv("HF_TOKEN") is None:
        raise ValueError("HF_TOKEN is not set")

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


def test_get_notes_by_description():
    
    fake_client = MagicMock()
    
    # Return different embeddings based on input text
    def mock_post(*args, **kwargs):
        # Handle both json={"inputs": text} and json_data={"inputs": text}
        json_data = kwargs.get("json", {})
        text = json_data.get("inputs", "")
        # Create a simple hash-based embedding to differentiate texts
        import hashlib
        hash_val = int(hashlib.md5(text.encode()).hexdigest()[:8], 16) % 1000
        # Return embedding with values based on text hash
        embedding = [hash_val / 1000.0] * 384
        return [embedding]
    
    fake_client.post.side_effect = mock_post
    
    # feature_extraction takes text directly as positional arg
    def mock_feature_extraction(text):
        import hashlib
        hash_val = int(hashlib.md5(text.encode()).hexdigest()[:8], 16) % 1000
        embedding = [hash_val / 1000.0] * 384
        return [embedding]
    
    fake_client.feature_extraction.side_effect = mock_feature_extraction

    with patch("semantic_search.InferenceClient", return_value=fake_client):
        client.post("/notes", json={"title": "This is dummy text to make sure the semantic search code doesn't crash.", "content": "This is a bunch of dummy text."})
        client.post("/notes", json={"title": "This is a random title", "content": "This is just some random text about nothing in particular."})
        response = client.get("/notes", params={"description": "Semantic search", "top_k": 1})

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1


def test_live_get_notes_by_description():
    if os.getenv("HF_TOKEN") is None:
        raise ValueError("HF_TOKEN is not set")

    try:
        with open("test_strings_multiple.txt", "r", encoding="utf-8") as f:
            contents = f.read().strip()
            if contents:
                for line in contents.split("\n"):
                    client.post("/notes", json={"title": "", "content": line})
    except FileNotFoundError:
        pass

    response = client.get("/notes", params={"description": "Semantic search", "top_k": 1})
    if response.status_code != 200:
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["content"].find("Semantic search") != -1