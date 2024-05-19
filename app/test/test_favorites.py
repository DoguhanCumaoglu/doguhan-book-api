from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_favorite():
    client.post("/users/register", json={"username": "testuser", "password": "password"})
    response = client.post("/users/login", data={"username": "testuser", "password": "password"})
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/books/",
        json={"title": "Test Book", "author": "Author", "isbn": "1234567890", "publication_year": 2021},
        headers=headers
    )
    book_id = response.json()["id"]

    response = client.post(f"/favorites/{book_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["book_id"] == book_id

# Add more tests for each endpoint and scenario
