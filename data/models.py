from django.db import models

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
    Country = models.CharField()
    iso2 = models.CharField('2 Digit ISO')
    iso3 = models.CharField('3 Digit ISO')
    un = models.IntegerField('United Nations Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name   
