import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Vertex AI & Gemini Grounding PoC" in response.text


def test_get_config():
    response = client.get("/api/config")
    assert response.status_code == 200
    data = response.json()
    assert "project_id" in data
    assert "location" in data
    assert "datastore_id" in data


def test_update_config():
    payload = {
        "project_id": "test-project-123",
        "location": "europe-west1",
        "datastore_id": "test-ds-456",
        "model_name": "gemini-2.0-flash",
    }
    response = client.post("/api/config", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["project_id"] == "test-project-123"
    assert data["location"] == "europe-west1"
    assert data["datastore_id"] == "test-ds-456"


def test_single_grounding_google_search():
    payload = {
        "prompt": "What is Vertex AI Grounding?",
        "mode": "google_search",
        "model_name": "gemini-2.0-flash",
    }
    response = client.post("/api/ground", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "google_search"
    assert "Google Search" in data["mode_title"]
    assert len(data["metadata"]["web_search_queries"]) > 0
    assert len(data["metadata"]["citations"]) > 0


def test_single_grounding_web_enterprise():
    payload = {
        "prompt": "Compliance policy for enterprise grounding",
        "mode": "web_enterprise",
        "model_name": "gemini-2.0-flash",
    }
    response = client.post("/api/ground", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "web_enterprise"
    assert "GCP Web Grounding Enterprise" in data["mode_title"]


def test_single_grounding_vertex_search():
    payload = {
        "prompt": "Internal architecture documents",
        "mode": "vertex_search",
        "model_name": "gemini-2.0-flash",
    }
    response = client.post("/api/ground", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "vertex_search"
    assert "Vertex AI Search" in data["mode_title"]


def test_compare_all_modes():
    payload = {
        "prompt": "Compare grounding methods",
        "model_name": "gemini-2.0-flash",
    }
    response = client.post("/api/compare", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "web_enterprise" in data["results"]
    assert "google_search" in data["results"]
    assert "vertex_search" in data["results"]


def test_empty_prompt_validation():
    payload = {"prompt": "  "}
    response = client.post("/api/ground", json=payload)
    assert response.status_code == 400
