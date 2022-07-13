from django.contrib.gis.db import models

# Create your models here.


class Country(models.Model):

	admin = models.CharField(max_length=255, blank=False, null=False)
	iso_a3 = models.CharField(max_length=255, blank=False, null=False)
	geom = models.MultiPolygonField(blank=False, null=False)

	def __str__(self):
		return f"{self.id}. {self.admin} {self.iso_a3}"

	class Meta:
		ordering = ['admin']