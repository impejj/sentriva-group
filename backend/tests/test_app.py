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


def assert_persisted(db_path, table, record_id, expected_tail):
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            f"SELECT id, source, schema_version, status, {expected_tail[0]} FROM {table} WHERE id = ?",
            (record_id,),
        ).fetchone()
    assert row is not None
    assert row[1:] == ("sentriva_web", 1, "RECEIVED", expected_tail[1])


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
    assert_persisted(
        db_path,
        "research_requests",
        body["data"]["id"],
        ("company", "Example Industrial SA"),
    )


def test_supplier_registration_persists_and_reads_back(tmp_path, monkeypatch):
    app_module, db_path = load_app(tmp_path, monkeypatch)
    payload = {
        "company": "Supplier Example SA",
        "country": "Argentina",
        "contact_name": "Lucía Gómez",
        "email": "lucia@example.com",
        "categories": "Utility poles; treated wood",
        "standards": "Technical documentation available on request",
    }
    with TestClient(app_module.app) as client:
        response = client.post("/api/v1/suppliers", json=payload)
    body = response.json()
    assert response.status_code == 201
    assert body["success"] is True
    assert_persisted(
        db_path,
        "supplier_registrations",
        body["data"]["id"],
        ("company", "Supplier Example SA"),
    )


def test_rfq_response_persists_and_reads_back(tmp_path, monkeypatch):
    app_module, db_path = load_app(tmp_path, monkeypatch)
    payload = {
        "product": "Utility pole",
        "quantity": "100",
        "unit": "units",
        "delivery_location": "Buenos Aires, Argentina",
        "unit_price": "125.50",
        "currency": "USD",
        "incoterm": "EXW",
    }
    with TestClient(app_module.app) as client:
        response = client.post("/api/v1/rfq-responses", json=payload)
    body = response.json()
    assert response.status_code == 201
    assert body["success"] is True
    assert_persisted(
        db_path,
        "rfq_responses",
        body["data"]["id"],
        ("product", "Utility pole"),
    )


def test_required_fields_rejected_for_all_intakes(tmp_path, monkeypatch):
    app_module, _ = load_app(tmp_path, monkeypatch)
    with TestClient(app_module.app) as client:
        assert client.post(
            "/api/v1/research-requests", json={"company": "Only company"}
        ).status_code == 422
        assert client.post(
            "/api/v1/suppliers", json={"company": "Only company"}
        ).status_code == 422
        assert client.post(
            "/api/v1/rfq-responses", json={"product": "Only product"}
        ).status_code == 422
