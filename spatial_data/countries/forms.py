from django import forms

from .models import Country


class CountryForm(forms.ModelForm):

	class Meta:
		model = Country
		fields = '__all__'


class UploadForm(forms.Form):
	geojson_file = forms.FileField()
