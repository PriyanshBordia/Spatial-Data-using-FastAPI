from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("country/add", views.add_country, name="add_country"),
    path("upload", views.upload, name="upload"),
    path("docs", views.docs, name="docs"),
]
