import json

from django.contrib import messages
from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.geos import Polygon
from django.http import HttpResponseRedirect
from django.shortcuts import render
from termcolor import cprint

from .forms import UploadForm
from .models import Country

# Create your views here.


def home(request):
	return render(request,"countries/home.html",context={"status": "All good."})


def upload(request):
	try:
		form = UploadForm()
		if request.method == "POST":
			form = UploadForm(request.POST)
			data = json.load(request.FILES["geojson_file"])["features"]
			for row in data:
				properties = row["properties"]
				geometry = row["geometry"]
				print(properties)
				# print(geometry)
				admin = properties.get("ADMIN")
				iso_a3 = properties.get("ISO_A3")
				print(geometry.get("type"), len(geometry.get("coordinates")))
				if geometry.get("type") == "Polygon":
					points = [geometry.get("coordinates")]
				elif geometry.get("type") == "MultiPolygon":
					points = geometry.get("coordinates")
				else:
					cprint(f"{admin} Error", "red")
				geom = MultiPolygon([Polygon(point[0]) for point in points])
				Country.objects.create(admin=admin, iso_a3=iso_a3, geom=geom)
			messages.success(request, "success")
		return render(request, "countries/upload.html", context={"form": form})
	except Exception as e:
		message = f"{e}"
		messages.error(request, message)
		return HttpResponseRedirect("../upload")
