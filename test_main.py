from fastapi.testclient import TestClient
from main import app

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
        "/notes",
        json={"title": "Test Note", "content": "Test content"}
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