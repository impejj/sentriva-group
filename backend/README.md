# SENTRIVA Intake API — non-production slice

Bounded implementation of `docs/BACKEND-INTEGRATION-CONTRACT.md`.

Implemented:
- `GET /health`
- `POST /api/v1/research-requests`
- `POST /api/v1/suppliers`
- `POST /api/v1/rfq-responses`
- SQLite persistence for local/non-production verification
- persistence readback before returning success
- required-field validation and persistence/readback tests for all three intake flows

Current QA:
- local suite: 5/5 PASS
- GitHub `SENTRIVA Backend Tests` is the branch gate for `backend/**`

Intentionally unchanged / not production-ready:
- public frontend remains `EMAIL_FALLBACK`
- no production deployment
- no public read/list endpoints for captured submissions
- no authentication/admin console
- no attachments
- SQLite is a bounded non-production persistence implementation, not the final production datastore decision

## Local test

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r backend/requirements-dev.txt
pytest -q backend/tests
```

A frontend switch to API mode requires a protected deployment, health verification, persistence/readback evidence and an explicit configuration/deployment gate. Until then the public site continues using corporate email fallback.
