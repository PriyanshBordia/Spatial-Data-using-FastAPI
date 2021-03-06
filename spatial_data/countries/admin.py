from django.contrib import admin

from .models import Country

# Register your models here.

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
	model: Country
	list_display = ['id', 'iso_a3', 'admin'] # [str(field.name) for field in Country._meta.fields if field.name != 'geom']
	search_fields = ['id', 'admin']
