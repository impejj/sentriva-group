import importlib
import sqlite3

from fastapi.testclient import TestClient


def load_app(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("SENTRIVA_DB_PATH", str(db_path))
    import backend.app as app_module
    importlib.reload(app_module)
    return app_module, db_path


def test_health(tmp_path, monkeypatch):
    app_module, _ = load_app(tmp_path, monkeypatch)
    with TestClient(app_module.app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "ok"


def test_research_request_persists_and_reads_back(tmp_path, monkeypatch):
    app_module, db_path = load_app(tmp_path, monkeypatch)
    payload = {
        "company": "Example Industrial SA",
        "contact_name": "Ana Pérez",
        "email": "ana@example.com",
        "research_question": "Compare sourcing alternatives for utility poles.",
        "geography": "Argentina",
    }
    with TestClient(app_module.app) as client:
        response = client.post("/api/v1/research-requests", json=payload)
    body = response.json()
    assert response.status_code == 201
    assert body["success"] is True
    assert body["data"]["status"] == "RECEIVED"

    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "SELECT id, source, schema_version, status, company FROM research_requests WHERE id = ?",
            (body["data"]["id"],),
        ).fetchone()
    assert row is not None
    assert row[1:] == ("sentriva_web", 1, "RECEIVED", "Example Industrial SA")


def test_required_fields_rejected(tmp_path, monkeypatch):
    app_module, _ = load_app(tmp_path, monkeypatch)
    with TestClient(app_module.app) as client:
        response = client.post("/api/v1/research-requests", json={"company": "Only company"})
    assert response.status_code == 422
