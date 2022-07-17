from django import forms

from .models import Country


class CountryForm(forms.ModelForm):

	class Meta:
		model = Country
		fields = '__all__'

class UploadForm(forms.ModelForm):
    geojson_file = forms.FileField()

    class Meta:
        model = Country
        fields = ["geojson_file"]
