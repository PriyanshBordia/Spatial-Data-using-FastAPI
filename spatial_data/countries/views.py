import json

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from utils.utility import get_cleaned_data

from .forms import CountryForm, UploadForm
from .models import Country

# Create your views here.


def home(request):
	return render(request, "countries/home.html", context={})


def add_country(request):
	try:
		country = Country()
		if request.method == "POST":
			form = CountryForm(request.POST, instance=country)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(reverse('home', args=()))
			else:
				form = CountryForm(instance=country)
				return render(request, "countries/add_country.html", context={"form": form})
		else:
			form = CountryForm(instance=country)
			return render(request, "countries/add_country.html", context={"form": form})
	except Exception as e:
		message = f"{e}"
		messages.error(request, message)
		return HttpResponseRedirect("../")


def upload(request):
	try:
		form = UploadForm()
		if request.method == "POST":
			form = UploadForm(request.POST)
			data = json.load(request.FILES["geojson_file"])["features"]
			data = get_cleaned_data(data)
			Country.objects.bulk_create(data, batch_size=100)
			messages.success(request, "success")
		return render(request, "countries/upload.html", context={"form": form})
	except Exception as e:
		message = f"{e}"
		messages.error(request, message)
		return HttpResponseRedirect("../upload")