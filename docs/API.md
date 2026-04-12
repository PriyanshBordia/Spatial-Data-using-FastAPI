# Spatial Data using FastAPI

A geospatial REST API and web interface for country boundary data.

## Quick Start

```shell
git clone https://github.com/PriyanshBordia/Spatial-Data-using-FastAPI.git
cd Spatial-Data-using-FastAPI
docker compose up -d --build
```

Seed the database:

```
GET http://localhost:8002/populate_data
```

## Environment Variables

```shell
export DB_NAME=spatial_data
export DB_USERNAME=postgres
export DB_PASSWORD=postgres
export DB_HOST=localhost
export DB_PORT=5432
export API_KEY=""  # Set to enable auth on write endpoints
```

## API Endpoints

### Read

```
GET /                                  # Health check
GET /populate_data                     # Seed database
GET /country/id/{id}                   # By ID
GET /country/code/{code}               # By ISO A3 code (case-insensitive)
GET /country/name/{name}               # By exact name
GET /country/name/contains/{fragment}  # Search by name
GET /countries?skip=0&limit=100        # Paginated list
GET /country/neighbors/{id}            # Bordering countries
```

### Write (require `X-API-Key` header when `API_KEY` is set)

```
POST   /country/create/      # Create country
PUT    /country/update/{id}   # Update country
DELETE /country/delete/{id}   # Delete country
```

### Web UI

```
GET  /web                # Home page
GET  /web/country/add    # Add country form
POST /web/country/add    # Submit new country
GET  /web/upload         # Upload form
POST /web/upload         # Bulk upload GeoJSON
```

## Sample Input

```json
{
  "admin": "Wakanda",
  "iso_a3": "WKA",
  "geom": {
    "type": "Polygon",
    "coordinates": [[[30, -1], [30, 1], [32, 1], [32, -1], [30, -1]]]
  }
}
```

Polygon geometries are automatically promoted to MultiPolygon.

## Response Format

### Success

```json
{
  "success": true,
  "message": "API is fast..",
  "meta": { "size": 1 },
  "result": [
    {
      "id": 1,
      "name": "India",
      "code": "IND",
      "coordinates": [...]
    }
  ]
}
```

### Error

```json
{
  "success": false,
  "error": {
    "message": ["Country with id: 0 does not exist."]
  }
}
```

## Running Tests

```shell
docker compose exec fastapi python3 -m pytest app/tests/ -v
```

38 integration tests using real PostGIS seed data.

## References

- [FastAPI](https://fastapi.tiangolo.com/)
- [PostGIS](http://postgis.net/)
- [GeoAlchemy2](https://geoalchemy-2.readthedocs.io/)
- [Shapely](https://shapely.readthedocs.io/)
