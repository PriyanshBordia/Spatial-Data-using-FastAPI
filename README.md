# Spatial Data using FastAPI

A geospatial REST API and web interface for managing country boundary data, built with FastAPI, PostGIS, SQLAlchemy, and GeoAlchemy2.

## Features

- Interactive 3D globe with clickable country boundaries (Globe.GL)
- Click a country to see details and neighbors in a sidebar
- Navigate between neighbors by clicking through the sidebar list
- Dark mode toggle with localStorage persistence
- REST API with CRUD operations for country geometries
- Spatial neighbor queries (find countries that share borders)
- Search by name, ISO code, or partial name match
- Paginated listing of all countries
- Web UI for adding countries and bulk-uploading GeoJSON files
- API key authentication for write operations
- Interactive API docs at `/docs`

## Quick Start

```shell
git clone https://github.com/PriyanshBordia/Spatial-Data-using-FastAPI.git
cd Spatial-Data-using-FastAPI
docker compose up -d --build
```

This starts **PostGIS** on port 5432 and **FastAPI** on port 8002.

Seed the database with 239 country boundaries:

```shell
curl http://localhost:8002/populate_data
```

Browse the interactive API docs at **http://localhost:8002/docs**

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/` | | Health check |
| GET | `/populate_data` | | Seed database from bundled GeoJSON |
| GET | `/country/id/{id}` | | Get country by ID |
| GET | `/country/code/{code}` | | Get country by ISO A3 code |
| GET | `/country/name/{name}` | | Get country by exact name |
| GET | `/country/name/contains/{name}` | | Search countries by name |
| GET | `/countries?skip=0&limit=100` | | List countries (paginated) |
| GET | `/country/neighbors/{id}` | | Find bordering countries |
| POST | `/country/create/` | API Key | Create a country |
| PUT | `/country/update/{id}` | API Key | Update a country |
| DELETE | `/country/delete/{id}` | API Key | Delete a country |

### Web UI

| URL | Description |
|-----|-------------|
| `/web` | 3D globe — click countries to explore |
| `/web/country/add` | Add a country via form |
| `/web/upload` | Bulk upload GeoJSON file |

All pages support dark mode via the toggle button (bottom-left).

### Sample Request

```shell
curl -X POST http://localhost:8002/country/create/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d '{
    "admin": "Wakanda",
    "iso_a3": "WKA",
    "geom": {
      "type": "Polygon",
      "coordinates": [[[30, -1], [30, 1], [32, 1], [32, -1], [30, -1]]]
    }
  }'
```

Polygon geometries are automatically promoted to MultiPolygon.

### Sample Response

```json
{
  "success": true,
  "message": "Country inserted successfully.",
  "meta": { "size": 1 },
  "result": [
    { "id": 240, "name": "Wakanda", "code": "WKA", "coordinates": [...] }
  ]
}
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_NAME` | PostgreSQL database name | (required) |
| `DB_USERNAME` | PostgreSQL username | (required) |
| `DB_PASSWORD` | PostgreSQL password | (required) |
| `DB_HOST` | PostgreSQL host | (required) |
| `DB_PORT` | PostgreSQL port | `5432` |
| `API_KEY` | API key for write endpoints | `""` (disabled) |

When `API_KEY` is set, `POST`, `PUT`, and `DELETE` endpoints require the `X-API-Key` header.

## Project Structure

```
FastAPI/src/app/
  main.py                 # App assembly
  config.py               # Settings from env vars
  core/
    exceptions.py         # Domain exceptions
    geometry.py           # Geometry normalization (Polygon -> MultiPolygon)
    dependencies.py       # FastAPI dependencies (DB session, API key auth)
  db/
    engine.py             # SQLAlchemy engine + session
    models.py             # Country ORM model
    schemas.py            # Pydantic schemas (input + response)
  services/
    country.py            # Business logic (CRUD, spatial queries, data loading)
  routes/
    api.py                # JSON API endpoints
    web.py                # HTML web UI endpoints
  templates/              # Jinja2 templates
  data/
    countries.geojson     # Seed data (255 countries)
  tests/
    conftest.py           # Pytest fixtures with seed data
    tests.py              # 38 integration tests
```

See [Architecture](docs/ARCHITECTURE.md) for layer diagrams and data flow traces.

## Running Tests

```shell
docker compose exec fastapi python3 -m pytest app/tests/ -v
```

Tests use real PostGIS seed data (no mocks). Fixtures create and destroy test countries in setup/teardown.

## Development

### Pre-commit Hooks

```shell
pip install pre-commit
pre-commit install
```

Runs [ruff](https://docs.astral.sh/ruff/) lint + format on every commit.

### Local Development (without Docker)

Requires PostgreSQL with PostGIS, GDAL, and GEOS installed locally.

```shell
cd FastAPI/src
pip install -r requirements.txt
export DB_NAME=spatial_data DB_USERNAME=postgres DB_PASSWORD=postgres DB_HOST=localhost DB_PORT=5432
uvicorn app.main:app --reload --port 8000
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md) — Layer diagram, data flows, DB schema, tech stack
- [Design Decisions](docs/DESIGN.md) — Key choices with context, alternatives, and trade-offs
- [API Reference](docs/API.md) — Endpoint listing, request/response examples

## References

- [FastAPI](https://fastapi.tiangolo.com/)
- [PostGIS](http://postgis.net/)
- [GeoAlchemy2](https://geoalchemy-2.readthedocs.io/)
- [Shapely](https://shapely.readthedocs.io/)
