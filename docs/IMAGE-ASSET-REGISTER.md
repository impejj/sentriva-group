# SENTRIVA — Image Asset Register

Status: `CANDIDATE / PREVIEW_ONLY`
Branch: `feat/sentriva-v1-evolution`
Rule: no externally hosted preview image is considered a production asset.

## Purpose

The Golden V1 visual direction combines technical/data composition with selective industrial editorial photography. Photography must add physical context and perceived quality without turning SENTRIVA into a generic construction/industrial stock-photo site.

## Current candidate assets

| ID | Surface | Role | Current source | Alt contract | Production target |
|---|---|---|---|---|---|
| IMG-SG-001 | Home hero | Technical verification / precision | `https://images.unsplash.com/photo-1764737734436-7eb904d3a4ab` | `Trabajo de precisión sobre planos técnicos` | `assets/images/sentriva-technical-verification.*` |
| IMG-SG-002 | Home editorial band | Manufacturing intelligence | `https://images.unsplash.com/photo-1764114235896-034c8772de01` | `Proceso industrial de corte de precisión sobre metal` | `assets/images/sentriva-manufacturing-intelligence.*` |
| IMG-SG-003 | Home editorial band | Infrastructure sourcing | `https://images.unsplash.com/photo-1784914180179-5e4509667037` | `Infraestructura industrial y equipos de gran escala` | `assets/images/sentriva-infrastructure-sourcing.*` |

## Promotion gate

Before any public production release:

1. Founder/Visual review selects or rejects each candidate.
2. Verify source/licensing and preserve provenance.
3. Download approved assets into the repository or governed media storage.
4. Produce responsive WebP/AVIF variants with an appropriate JPEG/WebP fallback when required.
5. Record dimensions, crop/focal strategy and mobile behavior.
6. Remove runtime dependency on third-party image hosting.
7. Run accessibility, broken-asset and performance checks.
8. Re-run visual comparison after localization; no material composition regression is allowed.

## Visual constraints

- No yellow-hard-hat / handshake / generic-office clichés.
- Prefer process, material, infrastructure, measurement and technical-detail imagery.
- Images are evidence of context, not evidence of SENTRIVA projects or clients.
- Never imply that an illustrated facility, machine or project belongs to SENTRIVA.
- Photography is subordinate to the institutional methodology and sourcing-intelligence positioning.

## Preview failure behavior

A broken external candidate image is a preview defect, not evidence that the Golden layout is absent. Until localization is complete, the review surface must explicitly distinguish `EXTERNAL_CANDIDATE` from `LOCAL_PRODUCTION_ASSET`.
