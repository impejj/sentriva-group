# SENTRIVA GROUP — Institutional Site

**Technical Intelligence · Strategic Sourcing · Market Research**

## Estado

- `main`: baseline original recibida el 2026-09-01.
- `feat/sentriva-v1-evolution`: evolución V1 en curso.
- Working product: institutional site + Research Intake + Supplier Registration + RFQ + first real research vertical + editorial Insights.

## V1 routes

- `/index.html` — Golden Home candidate.
- `/research.html` — Request Research / structured research brief.
- `/suppliers.html` — Supplier Registration.
- `/rfq.html` — structured Request for Quotation.
- `/utility-poles.html` — first real vertical: Infrastructure / Utility Poles.
- `/insights.html` — editorial hub.
- `/insight-rfq-tecnico.html` — technical RFQ structure.
- `/insight-tco.html` — purchase price vs total cost of acquisition.
- `/insight-supplier-benchmarking.html` — supplier benchmarking variables.
- `/review.html` — Founder Mobile Review Hub; development-only and `noindex`.

## Posicionamiento

SENTRIVA GROUP se presenta como firma de inteligencia técnica, strategic sourcing y market research. No se presenta como constructora, marketplace ni agencia.

## Regla de credibilidad

No inventar clientes, proyectos, obras, facturación, empleados, oficinas, certificaciones, premios, testimonios, logos ni casos ficticios. La credibilidad debe provenir de metodología, evidencia, profundidad técnica y calidad de producto.

## Formularios

Los tres formularios actuales definen el contrato de datos y la UX V1. Deliberadamente no afirman persistencia, recepción de archivos ni lifecycle RFQ hasta implementar backend/API.

## Sistema visual

- `styles-v050.css` — sistema baseline.
- `golden-v1.css` — capa Golden Home / premium B2B intelligence.

Dirección: engineering + intelligence + data + global sourcing + premium consulting, evitando clichés de constructora y SaaS genérico.

## Preview móvil

`review.html` concentra todas las superficies actuales para revisión rápida desde teléfono. No forma parte de la navegación pública.

Existe `.github/workflows/mobile-preview-pages.yml`, que publica la branch V1 mediante GitHub Pages. Pages ya está habilitado en el repositorio; para que la branch de preview pueda desplegar, el environment `github-pages` debe permitir explícitamente `feat/sentriva-v1-evolution` en Deployment branches and tags.

Hasta cerrar esa regla del environment, puede usarse un proxy de desarrollo de archivos raw como preview de emergencia. No es hosting de producción.

## Primera vertical real

`Infrastructure / Utility Poles` demuestra la metodología mediante un marco de comparación de materiales, variables técnicas, normas, supply, condiciones comerciales y logística. Es un caso de la metodología, no el límite de SENTRIVA.

## Insights

La sección editorial arranca con pocas piezas útiles, no con contenido genérico de relleno. Las primeras piezas cubren RFQ técnico comparable, costo total de adquisición y supplier benchmarking.

## Evolución prevista

V1 Institutional Website  
V2 Supplier Database  
V3 RFQ Management  
V4 Market Intelligence Portal  
V5 Supplier / Buyer Workspace  
V6 Data & Intelligence Platform

## Source of truth

No regenerar el sitio desde prompts, archivos HTML aislados o memoria de chat. La continuidad parte siempre de GitHub y de la branch vigente.

## Próximo slice productivo

1. Founder visual/credibility review de Golden Home.
2. Backend API + almacenamiento durable para Research/Supplier/RFQ.
3. Proyección de datos reales del research Utility Poles.
4. ES/EN + SEO/analytics de producción.
