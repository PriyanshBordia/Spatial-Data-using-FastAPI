# Design Decisions

Record of key architectural and design choices made during the project consolidation.

## 1. Drop Django, Keep FastAPI

**Decision:** Remove the Django web UI stack entirely and consolidate into a single FastAPI application.

**Context:** The project had two full application stacks — Django (web UI with forms) and FastAPI (REST API) — sharing a PostGIS database with zero shared code. This caused:
- 3 separate implementations of Polygon→MultiPolygon geometry normalization
- 2 model definitions for the same table (Django ORM + SQLAlchemy)
- Inconsistent environment variable names (`DB_HOSTNAME` vs `DB_HOST`)
- Any schema change required updates in 8 places across both stacks

**Alternatives considered:**
1. **Keep both, share code** — Extract a shared library. Rejected: different ORMs (Django ORM vs SQLAlchemy) make sharing models impractical.
2. **Drop FastAPI, keep Django** — Add Django REST Framework. Rejected: the project's primary value is the REST API (the repo is named "Spatial-Data-using-FastAPI"), and FastAPI's auto-docs, async support, and dependency injection are better suited.
3. **Drop Django, keep FastAPI** — Add Jinja2 templates for the web UI. Chosen: FastAPI natively supports Jinja2 templating, and the Django UI was only 3 simple views.

**Trade-off:** Lost Django admin (the built-in CRUD grid). Gained: single codebase, single model, single deployment, eliminated all code duplication.

## 2. Service Layer Returns Models, Not Dicts

**Decision:** Service functions (`services/country.py`) return SQLAlchemy model instances and raise domain exceptions. They never construct HTTP response dicts.

**Context:** The old `crud.py` wrapped every return value in `success_response(data=[format_country(country)])` or `error_response(error=[...])`. This meant:
- CRUD functions couldn't be reused outside HTTP context (CLI, background tasks, templates)
- Every test had to unwrap the response envelope to assert on data
- The response format was baked into 8 different functions

**Design:** The service layer is framework-agnostic. The route layer handles serialization:
- API routes: `ok(country)` wraps a model in the JSON envelope
- Web routes: pass models directly to Jinja2 templates
- Tests: assert on model attributes without parsing JSON

**Trade-off:** Routes have a small amount of try/except boilerplate to catch domain exceptions and format them. This is preferable to mixing HTTP concerns into business logic.

## 3. Domain Exceptions Over Error Dicts

**Decision:** Replace the `error_response()` dict pattern with typed exceptions (`NotFoundError`, `DuplicateError`, `InvalidGeometryError`).

**Context:** The old CRUD functions returned `{"success": False, "error": {"message": [...]}}` dicts for errors. Callers had to check `result["success"]` to know if the operation worked — a stringly-typed error channel.

**Design:** Service functions raise exceptions that the route layer catches and formats. This makes error paths explicit and composable:
```python
# Old: caller must check dict
result = crud.get_country_by_id(db, id)
if not result["success"]:
    # handle error...

# New: exception propagates naturally
country = country_service.get_by_id(db, id)  # raises NotFoundError
```

**Trade-off:** Every route handler needs a try/except block. This is more verbose than the old pattern but makes the control flow explicit and testable.

## 4. Unified Geometry Normalization

**Decision:** Single function `to_wkb_multipolygon()` in `core/geometry.py` replaces 3 scattered implementations.

**Context:** Geometry normalization (Polygon → MultiPolygon, GeoJSON → WKBElement) existed in:
1. `FastAPI/src/app/utils/utility.py:normalize_geometry` — returned `None` on error
2. `FastAPI/src/app/utils/utility.py:populate_data` — inline Shapely conversion
3. `spatial_data/utils/utility.py:get_cleaned_data` — Django GEOS conversion

All three did the same thing differently, with different error handling.

**Design:** One function, one behavior: raises `InvalidGeometryError` for unsupported types (instead of returning `None`). Used by both `create()`/`update()` service functions and the `populate_from_features()` bulk loader.

## 5. Backward-Compatible API Response Envelope

**Decision:** Preserve the exact `{"success", "message", "meta", "result"}` / `{"success", "error"}` response shape.

**Context:** External consumers and the 38-test suite depend on this envelope format. Changing it would break backward compatibility for no functional benefit.

**Design:** `ok()` and `err()` helper functions in `routes/api.py` produce the envelope. They are 4 lines each — trivial to change if the format ever needs updating, and the change happens in one place instead of 8 CRUD functions.

## 6. Seed Data With Duplicate Tolerance

**Decision:** `populate_from_features()` skips records with duplicate `iso_a3` or `admin` values instead of failing.

**Context:** The bundled `countries.geojson` contains 255 features, but several share the `iso_a3` code `-99` (for territories like "Ashmore and Cartier Islands", "US Naval Base Guantanamo Bay", etc.). The old `populate_data` function tried to insert all records in a single transaction, which failed on the first duplicate and rolled back everything — leaving the database empty.

**Design:** Pre-load existing codes/names from DB, track seen codes/names in Python sets during iteration, skip any feature that would violate uniqueness. This makes the endpoint idempotent — safe to call multiple times.

**Trade-off:** O(N) queries upfront to load existing records. Acceptable for a one-time seed operation with ~255 records.

## 7. Web Routes on `/web` Prefix

**Decision:** Web UI lives at `/web`, `/web/country/add`, `/web/upload`. API lives at `/`, `/country/...`, `/countries`.

**Context:** The API's root endpoint (`GET /`) returns the health check JSON `{"success": true, "message": "API is fast.."}`. The web home page needs a different response. They can't share the same path.

**Alternatives:**
1. **API at `/api`, web at `/`** — Would break backward compatibility for all API consumers.
2. **Content negotiation** (return HTML or JSON based on Accept header) — Complex, fragile, hard to test.
3. **Web at `/web`** — Clean separation, no backward compatibility break.

Chosen option 3.

## 8. Ruff Over Black+Flake8+isort

**Decision:** Use ruff as the single linting and formatting tool, configured via `pyproject.toml` with a pre-commit hook.

**Context:** The project had no linting or formatting configuration at all. The old CI workflow installed flake8 but never ran it.

**Design:** Ruff replaces black (formatting), flake8 (linting), isort (import sorting), and pyupgrade in a single tool. Configured rules: `E`, `W`, `F`, `I`, `UP`, `B`, `SIM`, `RUF`. Tab indentation preserved (existing project convention). `B008` ignored for FastAPI's `Depends()` pattern.

## 9. Test Strategy: Seed Data, No Mocks

**Decision:** Tests use real PostGIS seed data created/destroyed via pytest fixtures. No mocking of database, ORM, or geometry operations.

**Context:** The old test suite had 10 tests (3 were empty stubs) that depended on pre-existing database state (assumed country ID 1 was "India"). Tests were not self-contained.

**Design:**
- `conftest.py` creates 3 test countries with real MultiPolygon geometries (two adjacent for neighbor tests, one isolated)
- Fixtures handle setup and teardown via explicit `db.add()` / `db.query().delete()`
- Tests that create data via the API (POST) clean up after themselves
- The only non-seed configuration is the `api_key` fixture that temporarily sets `settings.API_KEY`

**Trade-off:** Tests require a running PostGIS database (Docker). Cannot run in CI without Docker. This is acceptable because the application is inherently dependent on PostGIS spatial operations — mocking them would test the mocks, not the code.
