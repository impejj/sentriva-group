from __future__ import annotations

import os
import sqlite3
import uuid
from contextlib import asynccontextmanager, contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field

DB_PATH = Path(os.getenv("SENTRIVA_DB_PATH", Path(__file__).with_name("sentriva_intake.db")))


class ResearchRequestIn(BaseModel):
    company: str = Field(min_length=1, max_length=200)
    contact_name: str = Field(min_length=1, max_length=200)
    email: EmailStr
    research_question: str = Field(min_length=1, max_length=5000)
    phone: str | None = Field(default=None, max_length=100)
    industry: str | None = Field(default=None, max_length=200)
    geography: str | None = Field(default=None, max_length=500)
    product: str | None = Field(default=None, max_length=500)
    requirements: str | None = Field(default=None, max_length=5000)
    comparison_variables: str | None = Field(default=None, max_length=5000)
    deadline: str | None = Field(default=None, max_length=100)
    volume: str | None = Field(default=None, max_length=200)
    decision: str | None = Field(default=None, max_length=2000)


class SupplierRegistrationIn(BaseModel):
    company: str = Field(min_length=1, max_length=200)
    country: str = Field(min_length=1, max_length=120)
    contact_name: str = Field(min_length=1, max_length=200)
    email: EmailStr
    categories: str = Field(min_length=1, max_length=2000)
    legal_name: str | None = Field(default=None, max_length=250)
    state: str | None = Field(default=None, max_length=120)
    city: str | None = Field(default=None, max_length=120)
    website: str | None = Field(default=None, max_length=500)
    role: str | None = Field(default=None, max_length=200)
    phone: str | None = Field(default=None, max_length=100)
    products: str | None = Field(default=None, max_length=5000)
    company_type: str | None = Field(default=None, max_length=200)
    capacity: str | None = Field(default=None, max_length=1000)
    moq: str | None = Field(default=None, max_length=500)
    lead_time: str | None = Field(default=None, max_length=500)
    coverage: str | None = Field(default=None, max_length=1000)
    markets: str | None = Field(default=None, max_length=1000)
    standards: str | None = Field(default=None, max_length=2000)
    certifications: str | None = Field(default=None, max_length=2000)
    commercial_terms: str | None = Field(default=None, max_length=2000)
    currency: str | None = Field(default=None, max_length=50)
    notes: str | None = Field(default=None, max_length=5000)


class RFQResponseIn(BaseModel):
    product: str = Field(min_length=1, max_length=500)
    quantity: str = Field(min_length=1, max_length=100)
    unit: str = Field(min_length=1, max_length=100)
    delivery_location: str = Field(min_length=1, max_length=500)
    unit_price: str = Field(min_length=1, max_length=100)
    currency: str = Field(min_length=1, max_length=50)
    application: str | None = Field(default=None, max_length=1000)
    description: str | None = Field(default=None, max_length=5000)
    standard: str | None = Field(default=None, max_length=1000)
    dimensions: str | None = Field(default=None, max_length=1000)
    required_date: str | None = Field(default=None, max_length=100)
    production_time: str | None = Field(default=None, max_length=500)
    stock: str | None = Field(default=None, max_length=500)
    transport: str | None = Field(default=None, max_length=2000)
    taxes: str | None = Field(default=None, max_length=1000)
    payment_terms: str | None = Field(default=None, max_length=2000)
    validity: str | None = Field(default=None, max_length=500)
    incoterm: str | None = Field(default=None, max_length=100)
    comments: str | None = Field(default=None, max_length=5000)


@contextmanager
def db_connection() -> Iterator[sqlite3.Connection]:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()


def initialize_database() -> None:
    with db_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS research_requests (
                id TEXT PRIMARY KEY, received_at TEXT NOT NULL, source TEXT NOT NULL,
                schema_version INTEGER NOT NULL, status TEXT NOT NULL,
                company TEXT NOT NULL, contact_name TEXT NOT NULL, email TEXT NOT NULL,
                phone TEXT, industry TEXT, geography TEXT, product TEXT,
                research_question TEXT NOT NULL, requirements TEXT,
                comparison_variables TEXT, deadline TEXT, volume TEXT, decision TEXT
            );
            CREATE TABLE IF NOT EXISTS supplier_registrations (
                id TEXT PRIMARY KEY, received_at TEXT NOT NULL, source TEXT NOT NULL,
                schema_version INTEGER NOT NULL, status TEXT NOT NULL,
                company TEXT NOT NULL, country TEXT NOT NULL, contact_name TEXT NOT NULL,
                email TEXT NOT NULL, categories TEXT NOT NULL, legal_name TEXT, state TEXT,
                city TEXT, website TEXT, role TEXT, phone TEXT, products TEXT,
                company_type TEXT, capacity TEXT, moq TEXT, lead_time TEXT, coverage TEXT,
                markets TEXT, standards TEXT, certifications TEXT, commercial_terms TEXT,
                currency TEXT, notes TEXT
            );
            CREATE TABLE IF NOT EXISTS rfq_responses (
                id TEXT PRIMARY KEY, received_at TEXT NOT NULL, source TEXT NOT NULL,
                schema_version INTEGER NOT NULL, status TEXT NOT NULL,
                product TEXT NOT NULL, quantity TEXT NOT NULL, unit TEXT NOT NULL,
                delivery_location TEXT NOT NULL, unit_price TEXT NOT NULL, currency TEXT NOT NULL,
                application TEXT, description TEXT, standard TEXT, dimensions TEXT,
                required_date TEXT, production_time TEXT, stock TEXT, transport TEXT, taxes TEXT,
                payment_terms TEXT, validity TEXT, incoterm TEXT, comments TEXT
            );
            """
        )
        conn.commit()


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(title="SENTRIVA Intake API", version="0.2.0", lifespan=lifespan)


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, __: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {"code": "INTERNAL_ERROR", "message": "Unexpected server error."},
            "meta": {"request_id": None},
        },
    )


def persist_record(table: str, record: dict[str, object]) -> dict:
    request_id = str(uuid.uuid4())
    record_id = str(uuid.uuid4())
    payload = {
        "id": record_id,
        "received_at": datetime.now(timezone.utc).isoformat(),
        "source": "sentriva_web",
        "schema_version": 1,
        "status": "RECEIVED",
        **record,
    }
    columns = list(payload)
    placeholders = ", ".join("?" for _ in columns)
    safe_tables = {"research_requests", "supplier_registrations", "rfq_responses"}
    if table not in safe_tables:
        raise ValueError("Unsupported persistence table")

    with db_connection() as conn:
        conn.execute(
            f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})",
            tuple(payload[column] for column in columns),
        )
        conn.commit()
        persisted = conn.execute(
            f"SELECT id, status FROM {table} WHERE id = ?", (record_id,)
        ).fetchone()

    if persisted is None:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "PERSISTENCE_READBACK_FAILED",
                    "message": "Submission could not be verified.",
                },
                "meta": {"request_id": request_id},
            },
        )

    return {
        "success": True,
        "data": {"id": persisted["id"], "status": persisted["status"]},
        "meta": {"request_id": request_id},
    }


@app.get("/health")
def health() -> dict:
    return {
        "success": True,
        "data": {"status": "ok", "mode": "NON_PRODUCTION"},
        "meta": {"service": "sentriva-intake-api"},
    }


@app.post("/api/v1/research-requests", status_code=201)
def create_research_request(payload: ResearchRequestIn) -> dict:
    return persist_record("research_requests", payload.model_dump(mode="json"))


@app.post("/api/v1/suppliers", status_code=201)
def create_supplier_registration(payload: SupplierRegistrationIn) -> dict:
    return persist_record("supplier_registrations", payload.model_dump(mode="json"))


@app.post("/api/v1/rfq-responses", status_code=201)
def create_rfq_response(payload: RFQResponseIn) -> dict:
    return persist_record("rfq_responses", payload.model_dump(mode="json"))
