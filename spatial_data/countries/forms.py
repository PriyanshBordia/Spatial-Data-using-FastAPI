from django import forms
from .models import Country


class UploadForm(forms.ModelForm):
    geojson_file = forms.FileField()

    class Meta:
        model = Country
        fields = ["geojson_file"]
