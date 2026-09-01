# SENTRIVA Intake API — non-production slice

Bounded implementation of `docs/BACKEND-INTEGRATION-CONTRACT.md`.

Implemented:
- `GET /health`
- `POST /api/v1/research-requests`
- SQLite persistence for local/non-production verification
- persistence readback before returning success
- validation tests

Not implemented / intentionally unchanged:
- supplier endpoint
- RFQ endpoint
- public frontend API mode
- production deployment
- attachments

## Local test

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r backend/requirements-dev.txt
pytest -q backend/tests
```

The public site remains in `EMAIL_FALLBACK` mode.
