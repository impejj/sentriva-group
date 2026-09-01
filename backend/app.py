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
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS research_requests (
                id TEXT PRIMARY KEY,
                received_at TEXT NOT NULL,
                source TEXT NOT NULL,
                schema_version INTEGER NOT NULL,
                status TEXT NOT NULL,
                company TEXT NOT NULL,
                contact_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                industry TEXT,
                geography TEXT,
                product TEXT,
                research_question TEXT NOT NULL,
                requirements TEXT,
                comparison_variables TEXT,
                deadline TEXT,
                volume TEXT,
                decision TEXT
            )
            """
        )
        conn.commit()


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(title="SENTRIVA Intake API", version="0.1.0", lifespan=lifespan)


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


@app.get("/health")
def health() -> dict:
    return {
        "success": True,
        "data": {"status": "ok", "mode": "NON_PRODUCTION"},
        "meta": {"service": "sentriva-intake-api"},
    }


@app.post("/api/v1/research-requests", status_code=201)
def create_research_request(payload: ResearchRequestIn) -> dict:
    request_id = str(uuid.uuid4())
    record_id = str(uuid.uuid4())
    received_at = datetime.now(timezone.utc).isoformat()
    record = payload.model_dump()

    with db_connection() as conn:
        conn.execute(
            """
            INSERT INTO research_requests (
                id, received_at, source, schema_version, status,
                company, contact_name, email, phone, industry, geography, product,
                research_question, requirements, comparison_variables, deadline,
                volume, decision
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record_id,
                received_at,
                "sentriva_web",
                1,
                "RECEIVED",
                record["company"],
                record["contact_name"],
                str(record["email"]),
                record["phone"],
                record["industry"],
                record["geography"],
                record["product"],
                record["research_question"],
                record["requirements"],
                record["comparison_variables"],
                record["deadline"],
                record["volume"],
                record["decision"],
            ),
        )
        conn.commit()
        persisted = conn.execute(
            "SELECT id, status FROM research_requests WHERE id = ?", (record_id,)
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
