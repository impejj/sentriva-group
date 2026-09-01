from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = (ROOT / "script-v050.js").read_text(encoding="utf-8")


def read_page(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def test_public_submission_mode_fails_closed_to_email() -> None:
    assert "window.__SENTRIVA_SUBMISSION_MODE__ === 'API'" in SCRIPT
    assert ": 'EMAIL_FALLBACK'" in SCRIPT
    assert "new URLSearchParams" not in SCRIPT
    assert "form.reset(" not in SCRIPT
    assert "window.location.href = buildEmailHref(form)" in SCRIPT


def test_api_mode_requires_explicit_base_and_verified_success() -> None:
    assert "window.__SENTRIVA_API_BASE__" in SCRIPT
    assert "API_BASE_MISSING" in SCRIPT
    assert "result?.success !== true" in SCRIPT
    assert "!result?.data?.id" in SCRIPT
    assert "Sus datos siguen en el formulario" in SCRIPT
    assert "Usar envío por email" in SCRIPT


def test_all_public_forms_declare_email_default_and_canonical_endpoint() -> None:
    expected = {
        "research.html": "/api/v1/research-requests",
        "suppliers.html": "/api/v1/suppliers",
        "rfq.html": "/api/v1/rfq-responses",
    }
    for page_name, endpoint in expected.items():
        page = read_page(page_name)
        assert 'data-email-form' in page
        assert 'data-submission-default="EMAIL_FALLBACK"' in page
        assert f'data-api-endpoint="{endpoint}"' in page
        assert 'data-recipient="research@sentrivagroup.com"' in page


def test_frontend_payload_field_names_match_backend_contract_locators() -> None:
    research = read_page("research.html")
    for field in ("company", "contact_name", "email", "research_question"):
        assert f'name="{field}"' in research

    suppliers = read_page("suppliers.html")
    for field in ("company", "country", "contact_name", "email", "categories"):
        assert f'name="{field}"' in suppliers

    rfq = read_page("rfq.html")
    for field in ("product", "quantity", "unit", "delivery_location", "unit_price", "currency"):
        assert f'name="{field}"' in rfq
