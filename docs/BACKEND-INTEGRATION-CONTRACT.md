# SENTRIVA GROUP — Backend Integration Contract

Status: `READY_FOR_DELEGATED_EXECUTION / NON_PRODUCTION`
Version: `0.1`
Date: `2026-09-01`
Scope: Research Intake + Supplier Registration + RFQ Response

## 1. Purpose

Define the durable, bounded transition from the current honest email-based form flow to a future API-backed intake layer, without changing the public behavior until persistence is implemented, tested and explicitly enabled.

This document is an implementation contract and locator. It does **not** claim that a backend exists today.

## 2. Current verified state

Public forms:

- `research.html` — Research Intake
- `suppliers.html` — Supplier Registration
- `rfq.html` — RFQ Response

Current submission adapter:

- `script-v050.js`
- selector: `[data-email-form]`
- current mode: `EMAIL_FALLBACK`
- current verified recipient: `research@sentrivagroup.com`

The current adapter validates required HTML fields and prepares a `mailto:` message. It does not persist data and must remain the public default until the API gate below passes.

## 3. Implementation locators

Frontend integration locator:

- `script-v050.js`

Backend implementation locator reserved for the next bounded slice:

- `backend/`

Backend contract and evidence locator:

- `docs/BACKEND-INTEGRATION-CONTRACT.md`

No code outside these bounded locators should be changed for the first backend slice unless a concrete dependency requires it and is documented in the PR.

## 4. API boundary

Initial non-production API contract:

- `POST /api/v1/research-requests`
- `POST /api/v1/suppliers`
- `POST /api/v1/rfq-responses`
- `GET /health`

Initial response envelope:

```json
{
  "success": true,
  "data": {
    "id": "<server-generated-id>",
    "status": "RECEIVED"
  },
  "meta": {
    "request_id": "<request-id>"
  }
}
```

Failure responses must return `success=false` and a stable error code. The frontend must never display success before a successful API response.

## 5. Research Request payload

Source: current `research.html` field names.

Required:

- `company`
- `contact_name`
- `email`
- `research_question`

Optional:

- `phone`
- `industry`
- `geography`
- `product`
- `requirements`
- `comparison_variables`
- `deadline`
- `volume`
- `decision`

Server metadata to add on receipt:

- `id`
- `received_at`
- `source = sentriva_web`
- `schema_version = 1`
- `status = RECEIVED`

## 6. Supplier payload

Source: current `suppliers.html` field names.

Required:

- `company`
- `country`
- `contact_name`
- `email`
- `categories`

Optional:

- `legal_name`
- `state`
- `city`
- `website`
- `role`
- `phone`
- `products`
- `company_type`
- `capacity`
- `moq`
- `lead_time`
- `coverage`
- `markets`
- `standards`
- `certifications`
- `commercial_terms`
- `currency`
- `notes`

Server metadata:

- `id`
- `received_at`
- `source = sentriva_web`
- `schema_version = 1`
- `status = RECEIVED`

Registration does not imply homologation, recommendation or commercial approval. No backend/UI state may imply otherwise.

## 7. RFQ Response payload

Source: current `rfq.html` field names.

Required:

- `product`
- `quantity`
- `unit`
- `delivery_location`
- `unit_price`
- `currency`

Optional:

- `application`
- `description`
- `standard`
- `dimensions`
- `required_date`
- `production_time`
- `stock`
- `transport`
- `taxes`
- `payment_terms`
- `validity`
- `incoterm`
- `comments`

Server metadata:

- `id`
- `received_at`
- `source = sentriva_web`
- `schema_version = 1`
- `status = RECEIVED`

A received RFQ response is evidence supplied by a source; it is not automatically validated technical truth.

## 8. Attachments

Attachments are explicitly OUT OF SCOPE for the first persistence slice.

Until governed upload/storage, malware scanning, size/type policy and access control exist, the public flow continues instructing users to attach technical documents to the corresponding corporate email.

Do not implement ad-hoc public file upload in the first slice.

## 9. Frontend transition rule

The first API integration must preserve an explicit submission mode.

Recommended contract:

- default: `EMAIL_FALLBACK`
- non-production test: `API`
- API failure before production enablement: do not lose entered form data; offer email fallback

The public site must not claim persistence while `EMAIL_FALLBACK` is active.

## 10. Minimum backend gates

Before any public form switches to API mode:

1. `/health` passes in the target environment.
2. All three endpoint schemas have validation tests.
3. Required-field rejection tests pass.
4. Successful submissions return a durable server-generated ID.
5. Persistence readback proves the record exists after write.
6. Duplicate/retry behavior is defined.
7. CORS/origin policy is restricted to approved SENTRIVA origins.
8. Basic abuse/rate limiting is present.
9. Logs exclude unnecessary sensitive payload data.
10. Error responses do not leak infrastructure details.
11. A rollback to `EMAIL_FALLBACK` is tested.
12. Public copy remains free of prototype/backend/internal-roadmap language.

## 11. Persistence principles

The first slice should persist the smallest useful canonical record for each intake type. Do not build CRM, supplier scoring, workflow automation or a full research platform in this slice.

Separate:

`RECEIVED DATA` → `VALIDATED / ENRICHED DATA` → `ANALYTICAL CONCLUSIONS`

Never convert supplier-provided claims into verified facts automatically.

## 12. Security / privacy baseline

- Data minimization: persist only fields in this contract plus required technical metadata.
- Do not store email content or attachments redundantly in the first slice.
- Do not expose intake records from public GET endpoints.
- No secrets in repository/client JavaScript.
- Production secrets belong in the deployment secret store.
- Preserve traceability for creation time and request ID.

## 13. First bounded implementation slice

Authorized next reversible unit:

1. Create `backend/` skeleton in a non-production branch context.
2. Implement `/health`.
3. Implement **one** endpoint first: `POST /api/v1/research-requests`.
4. Add schema/validation tests.
5. Add persistence + readback test in a non-production datastore.
6. Cross-QA Engineering → QA.
7. Do not switch the public form from `EMAIL_FALLBACK` yet.
8. Persist evidence and exact rollback.

Only after this first endpoint passes should Supplier and RFQ reuse the same pattern.

## 14. Definition of done for the first slice

PASS requires an output independent of runtime reporting:

- backend code under `backend/`;
- tests;
- non-production persistence evidence;
- readback verification;
- no public behavior change;
- no merge/deploy to production;
- PR evidence with next action.

## 15. Rollback

The current public forms remain operational through `mailto:`. Therefore the first backend slice is additive and reversible: remove/disable the non-production backend integration and retain `EMAIL_FALLBACK` unchanged.
