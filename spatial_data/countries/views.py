from django.shortcuts import render

# Create your views here.


def home(request):
	return render(request, "countries/home.html", context={"status": "All good."})
