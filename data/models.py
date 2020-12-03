from django.db import models
from django.contrib.gis.db import models


class SBPRI(models.Model):
    date = models.DateField()
    Bolivia = models.DecimalField(max_digits=8, decimal_places=5)
    Uruguay = models.DecimalField(max_digits=8, decimal_places=5)
    Paraguay = models.DecimalField(max_digits=8, decimal_places=5)
    Venezuela = models.DecimalField(max_digits=8, decimal_places=5)
    Colombia = models.DecimalField(max_digits=8, decimal_places=5)
    Ecuador = models.DecimalField(max_digits=8, decimal_places=5)
    Peru = models.DecimalField(max_digits=8, decimal_places=5)
    Chile = models.DecimalField(max_digits=8, decimal_places=5)
    Argentina = models.DecimalField(max_digits=8, decimal_places=5)
    Mexico = models.DecimalField(max_digits=8, decimal_places=5)


class WorldBorder(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2, null=True)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name   
