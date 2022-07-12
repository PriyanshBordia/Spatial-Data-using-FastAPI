from django.contrib.gis.db import models

# Create your models here.


class Country(models.Model):

	ogc_fid = model.IntegerField()
	admin = models.CharField()
	iso_a3 = models.CharField()
	geom = models.PolygonField()

	class Meta:
		db_table = "polygon"
		managed = False
		verbose_name = "polygon"
		verbose_name_plural = "polygons"
