# 3D Globe UI — Design Spec

## Goal

Replace the current Bootstrap card-based home page with an interactive 3D globe that renders country boundaries from the PostGIS database. Clicking a country opens a sidebar with details and a clickable neighbor list.

## Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Pin behavior | Click existing countries to see info | Primary dataset is countries; no new entity types |
| Country rendering | Flat-colored polygons on globe surface | Clean, functional, matches minimal UI style |
| Click action | Sidebar panel with details + neighbors | Rich info without cluttering the globe |
| Page location | Replaces `/web` home page | Globe IS the main experience |
| Visual style | Minimal/clean — neutral globe, flat colors | Matches existing Bootstrap UI feel |
| Library | Globe.GL (Three.js wrapper) | Purpose-built for data globes, GeoJSON support, ~200KB |

## Components

### Globe (main viewport)

- Renders all countries as colored polygons via Globe.GL's `polygonsData` layer
- Data loaded from `GET /countries?limit=300` on page load
- Coordinates from API response converted to GeoJSON Features client-side
- Slow auto-rotation on idle, stops on user interaction
- Click polygon → highlight it, fly camera to centroid, open sidebar
- Light/neutral sphere color, no satellite texture

### Sidebar (right panel)

- Slides in from right on country click
- Shows: country name (large), ISO A3 code, country ID
- Neighbor section: fetched from `GET /country/neighbors/{id}`
- Each neighbor rendered as a clickable item — clicking it flies the globe to that country and loads its details
- Close button (X) collapses sidebar back
- Scrollable if neighbor list is long

### Navbar (top)

- Same Bootstrap 4 navbar as current
- Brand "Spatial Data" → resets globe to default view
- Links: Add Country, Upload, API Docs
- No changes to existing navbar markup

## Data Flow

```
Page load:
  1. Fetch GET /countries?limit=300
  2. Transform response.result[] into GeoJSON Features
  3. Pass to Globe.GL polygonsData

Country click:
  1. Highlight clicked polygon (accent color)
  2. Fly camera to polygon centroid
  3. Fetch GET /country/neighbors/{id}
  4. Render sidebar with country info + neighbor list

Neighbor click:
  1. Same as country click — highlight, fly, fetch, render
```

## Technical Approach

- **No build step** — vanilla JS, Globe.GL loaded from CDN
- **Single template rewrite** — only `home.html` changes substantially
- **Existing API** — no new endpoints needed
- **GeoJSON construction** — API returns `{id, name, code, coordinates}`, JS wraps into `{type: "Feature", geometry: {type: "MultiPolygon", coordinates}, properties: {id, name, code}}`

## Files Changed

| File | Change |
|------|--------|
| `templates/home.html` | Rewrite — globe container + sidebar + JS |
| `templates/base.html` | Minor — full-viewport body style for globe page |
| `routes/web.py` | Unchanged |
| `routes/api.py` | Unchanged |
| All other files | Unchanged |

## Out of Scope

- New API endpoints
- New DB models or tables
- Build tooling (webpack, vite, etc.)
- User accounts or saved pins
- Custom pin/marker placement
