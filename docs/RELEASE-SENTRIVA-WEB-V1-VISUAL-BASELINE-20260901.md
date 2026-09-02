# SENTRIVA GROUP — Web V1 Visual Baseline

Status: CANONICAL RELEASE BASELINE
Date: 2026-09-01
Repository: impejj/sentriva-group
Target branch: main

## Purpose

Normalize and preserve the approved SENTRIVA public website visual baseline after iterative local and online QA.

## Canonical visual state

The approved baseline keeps the existing information architecture and business flows while applying the accepted visual refinement to:

1. balanced industrial image band;
2. richer Capabilities composition;
3. Markets visual system;
4. Methodology journey;
5. Utility Poles visual research block;
6. Supplier Intelligence visual block;
7. stronger closing CTA/footer composition.

## Production assets

Local first-party image assets replace the previous dependency on Unsplash for the principal homepage imagery:

- `assets/images/sentriva-hero-technical-intelligence-v2.webp`
- `assets/images/sentriva-manufacturing-intelligence-v2.webp`
- `assets/images/sentriva-infrastructure-sourcing-v2.webp`
- `assets/images/sentriva-supplier-intelligence-v1.webp`
- `assets/images/sentriva-utility-poles-research-v1.webp`

These images are project-owned generated visual assets and are stored inside the repository for deterministic deployment.

## Versioned web assets

The baseline references versioned public assets to avoid stale browser/CDN caches:

- `styles-v051.css`
- `golden-v101.css`
- `visual-refinement-v1.css`
- `script-v051.js`

Legacy v050/v1 assets remain in the repository temporarily for rollback compatibility, but the current homepage references the versioned baseline above.

## Governance rule

GitHub `main` is the source of truth for the public website. Local workspace and deploy ZIPs must be generated from `main`, not used as an independent source of truth.

No future visual release may replace the approved baseline with an older local snapshot. Changes must be incremental, tested locally, committed, and then deployed from GitHub.
