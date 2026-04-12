# Architecture

## Overview

Single FastAPI application serving a JSON REST API and an HTML web interface, backed by a PostGIS database for geospatial country boundary data.

```
                    ┌─────────────┐
                    │   Clients   │
                    └──────┬──────┘
                           │
              ┌────────────┴────────────┐
              │                         │
     JSON requests              Browser requests
              │                         │
    ┌─────────▼─────────┐    ┌─────────▼─────────┐
    │   routes/api.py   │    │   routes/web.py   │
    │   11 endpoints    │    │   5 endpoints     │
    │   ok()/err()      │    │   Jinja2Templates │
    └─────────┬─────────┘    └─────────┬─────────┘
              │                         │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │  services/country.py    │
              │  Business logic layer   │
              │  Returns ORM models     │
              │  Raises domain errors   │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │   core/geometry.py      │
              │   Polygon→MultiPolygon  │
              │   GeoJSON→WKBElement    │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │   db/models.py          │
              │   db/engine.py          │
              │   SQLAlchemy + PostGIS  │
              └────────────┬────────────┘
                           │
                    ┌──────▼──────┐
                    │   PostGIS   │
                    └─────────────┘
```

## Layers

### Presentation Layer (`routes/`)

Two routers mounted on a single FastAPI app:

**`routes/api.py`** — JSON API with envelope pattern:
- Every response wraps data in `{"success": bool, "meta": {"size": N}, "result": [...]}` or `{"success": false, "error": {"message": [...]}}`
- `ok()`, `ok_raw()`, `err()` helper functions build the envelope
- Write endpoints protected by optional `verify_api_key` dependency
- Routes are thin: call service, wrap result, catch domain exceptions

**`routes/web.py`** — HTML pages via Jinja2:
- Serves forms for adding countries and uploading GeoJSON
- Uses the same service layer as the API — no duplicated logic
- Templates in `templates/` with Bootstrap 4 CDN

### Service Layer (`services/country.py`)

Pure business logic. Key contract:
- **Returns** ORM model instances (`Country`) or lists thereof
- **Raises** domain exceptions (`NotFoundError`, `DuplicateError`, `InvalidGeometryError`)
- **Never** builds HTTP responses, dicts, or envelopes

Functions:

| Function | Purpose |
|----------|---------|
| `get_by_id(db, id)` | Single country by primary key |
| `get_by_code(db, code)` | Single country by ISO A3 (case-insensitive) |
| `get_by_name(db, name)` | Single country by exact name |
| `search_by_name(db, fragment)` | Countries matching substring |
| `get_all(db, skip, limit)` | Paginated listing |
| `create(db, data)` | Insert with duplicate check + geometry validation |
| `update(db, id, data)` | Update with duplicate check + geometry validation |
| `delete(db, id)` | Delete, returns snapshot of deleted record |
| `get_neighbors(db, id)` | Spatial intersection query |
| `populate_from_features(db, features)` | Bulk insert from GeoJSON features, skips duplicates |
| `populate_from_geojson(db, path)` | Load features from file, delegates to `populate_from_features` |

### Core Layer (`core/`)

Cross-cutting concerns shared by services and routes:

**`core/geometry.py`** — Single source of truth for geometry normalization:
- `to_wkb_multipolygon(geom_dict)` — GeoJSON dict → WKBElement, auto-promotes Polygon to MultiPolygon
- `extract_coordinates(wkb)` — WKBElement → coordinate arrays for API responses

**`core/exceptions.py`** — Domain exceptions:
- `NotFoundError(entity, identifier)` — 404-equivalent
- `DuplicateError(entity, detail)` — Unique constraint violation
- `InvalidGeometryError(detail)` — Unsupported geometry type

**`core/dependencies.py`** — FastAPI dependency injection:
- `get_db()` — Yields SQLAlchemy session, closes on completion
- `verify_api_key()` — Validates `X-API-Key` header when `API_KEY` env var is set

### Infrastructure Layer (`db/`)

**`db/engine.py`** — SQLAlchemy engine, session factory, declarative Base
**`db/models.py`** — `Country` ORM model (table: `countries_country`)
**`db/schemas.py`** — Pydantic models for request validation and response serialization

## Data Flow

### API Read Request

```
GET /country/code/IND
  → api.get_country_code(code="IND", db=session)
    → country_service.get_by_code(db, "IND")
      → db.query(Country).filter(iso_a3 == "IND").one_or_none()
      → returns Country instance (or raises NotFoundError)
    → ok(country)
      → CountryResponse.from_orm_model(country)
      → {"success": true, "result": [{"id": ..., "name": "India", ...}]}
```

### API Write Request

```
POST /country/create/  (X-API-Key: secret)
  → verify_api_key() — checks header against settings.API_KEY
  → api.create_country(country=CountryCreate, db=session)
    → country_service.create(db, data)
      → checks for duplicate admin/iso_a3
      → to_wkb_multipolygon(data.geom)  — validates + converts geometry
      → db.add(Country(...)) → db.commit()
      → returns Country instance (or raises DuplicateError/InvalidGeometryError)
    → ok(country, "Country inserted successfully.")
```

### Web Upload

```
POST /web/upload  (multipart form with .geojson file)
  → web.upload_submit(geojson_file=UploadFile)
    → json.loads(file contents) → features list
    → country_service.populate_from_features(db, features)
      → skips duplicates (checks existing + seen sets)
      → Polygon → MultiPolygon promotion for each feature
      → bulk db.add() → single db.commit()
      → returns count
    → TemplateResponse("upload.html", messages=[...])
```

### Globe Interaction (client-side)

```
Page load (/web):
  1. Browser loads Globe.GL from CDN
  2. JS fetches GET /countries?limit=300
  3. Transforms API response into GeoJSON Features
  4. Globe.GL renders polygons on 3D sphere

Country click:
  1. Globe.GL fires onPolygonClick callback
  2. JS computes centroid, flies camera to country
  3. JS fetches GET /country/neighbors/{id}
  4. Sidebar renders country info + clickable neighbor list

Neighbor click:
  1. Same flow — highlight, fly-to, fetch neighbors, update sidebar

Theme toggle:
  1. Click dispatches 'themechange' CustomEvent
  2. base.html script toggles body.dark class + localStorage
  3. Globe page listener updates WebGL colors (globe material, polygon colors, atmosphere)
  4. CSS custom properties handle sidebar, navbar, forms, alerts
```

## Database

Single table: `countries_country`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | Integer | Primary key, auto-increment |
| `admin` | String | Unique, not null — country name |
| `iso_a3` | String | Unique, not null — ISO 3166-1 alpha-3 code |
| `geom` | MultiPolygon (SRID 4326) | Not null — country boundary geometry |

The table name `countries_country` is inherited from the original Django migration and preserved for backward compatibility. It is configurable via `settings.MODEL_NAME`.

## Authentication

Optional API key authentication, controlled by the `API_KEY` environment variable:

- **When `API_KEY` is empty (default):** All endpoints are open. Suitable for development.
- **When `API_KEY` is set:** `POST`, `PUT`, `DELETE` API endpoints require `X-API-Key` header matching the configured value. Read endpoints and web UI remain open.

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI 0.124 |
| 3D Globe | Globe.GL 2.45 (Three.js wrapper, CDN) |
| ORM | SQLAlchemy 2.0 |
| Spatial DB | PostGIS (via GeoAlchemy2 0.18) |
| Geometry | Shapely 2.x |
| Templates | Jinja2 |
| Validation | Pydantic 2.x |
| Server | Uvicorn 0.40 |
| Database | PostgreSQL + PostGIS |
| Container | Docker Compose |
| Linting | Ruff (pre-commit) |
| Testing | Pytest with real PostGIS seed data |
| Theming | CSS custom properties + localStorage |
