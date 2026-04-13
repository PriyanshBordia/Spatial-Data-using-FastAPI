import json

from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from ..core.dependencies import get_db
from ..core.exceptions import DuplicateError, InvalidGeometryError
from ..db import schemas
from ..services import country as country_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/web", response_class=HTMLResponse, name="web_home")
async def home(request: Request):
	return templates.TemplateResponse("home.html", {"request": request})


@router.get("/web/country/add", response_class=HTMLResponse, name="add_country_form")
async def add_country_form(request: Request):
	return templates.TemplateResponse(
		"add_country.html",
		{
			"request": request,
			"errors": [],
			"admin": "",
			"iso_a3": "",
			"geom": "",
		},
	)


@router.post("/web/country/add", response_class=HTMLResponse, name="add_country_submit")
async def add_country_submit(
	request: Request,
	admin: str = Form(...),
	iso_a3: str = Form(...),
	geom: str = Form(...),
	db: Session = Depends(get_db),
):
	try:
		geom_dict = json.loads(geom)
		country_service.create(db, schemas.CountryCreate(admin=admin, iso_a3=iso_a3, geom=geom_dict))
		return RedirectResponse(url="/web", status_code=303)
	except (DuplicateError, InvalidGeometryError, json.JSONDecodeError, ValueError) as e:
		return templates.TemplateResponse(
			"add_country.html",
			{
				"request": request,
				"errors": [str(e)],
				"admin": admin,
				"iso_a3": iso_a3,
				"geom": geom,
			},
		)


@router.get("/web/upload", response_class=HTMLResponse, name="upload_form")
async def upload_form(request: Request):
	return templates.TemplateResponse("upload.html", {"request": request, "messages": []})


@router.post("/web/upload", response_class=HTMLResponse, name="upload_submit")
async def upload_submit(
	request: Request,
	geojson_file: UploadFile = File(...),
	db: Session = Depends(get_db),
):
	messages = []
	if not geojson_file.filename.endswith((".geojson", ".json")):
		messages.append({"type": "error", "text": "Only .geojson and .json files are accepted."})
		return templates.TemplateResponse("upload.html", {"request": request, "messages": messages})
	try:
		contents = await geojson_file.read()
		features = json.loads(contents)["features"]
		count = country_service.populate_from_features(db, features)
		messages.append({"type": "success", "text": f"Uploaded {count} countries successfully."})
	except Exception:
		messages.append({"type": "error", "text": "Failed to process upload. Check that the file is valid GeoJSON."})
	return templates.TemplateResponse("upload.html", {"request": request, "messages": messages})
