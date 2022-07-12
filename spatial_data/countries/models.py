from django.contrib.gis.db import models

# Create your models here.


class Country(models.Model):

	ogc_fid = models.IntegerField()
	admin = models.CharField(max_length=255)
	iso_a3 = models.CharField(max_length=255)
	geom = models.PolygonField()

    class Meta:
        db_table = "polygon"
        managed = False
        verbose_name = "polygon"
        verbose_name_plural = "polygons"
