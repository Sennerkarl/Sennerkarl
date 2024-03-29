from django.db import models

class SBPRI(models.Model):
    date = models.DateField()
    Bolivia = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True, default='nan')
    Uruguay = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True, default='nan')
    Paraguay = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True, default='nan')
    Venezuela = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True, default='nan')
    Colombia = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True, default='nan')
    Ecuador = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True, default='nan')
    Peru = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True, default='nan')
    Chile = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True, default='nan')
    Argentina = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True, default='nan')
    Mexico = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True, default='nan')
    Canada = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True, default='nan')
    Australia = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True, default='nan')
    India = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True, default='nan')
    Pakistan = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True, default='nan')
    Ireland = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True, default='nan')
    United_States = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True, default='nan')
    New_Zealand = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True, default='nan')
    South_Africa = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True, default='nan')
    Singapore = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True, default='nan')
    Germany = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True, default='nan')
    Austria = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True, default='nan')
    Switzerland = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True, default='nan')
    Spain = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True, default='nan')

continent_choices= (
                    ('south america', 'south america'),
                    ('north america', 'north america'),
                    ('europe', 'europe'),
                    ('africa', 'africa'),
                    ('asia', 'asia'),
                    ('world', 'world')
                        )

class WorldBorder(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=100)
    iso2 = models.CharField('2 Digit ISO', max_length=5)
    iso3 = models.CharField('3 Digit ISO', max_length=5)
    un = models.IntegerField('United Nations Code')
    lon = models.FloatField()
    lat = models.FloatField()
    flag = models.ImageField(upload_to='flags', default='worldmap_02.png')
    ctryimg = models.ImageField(upload_to='ctryimg', default='worldmap_02.png')
    continent = models.CharField(choices=continent_choices, default="world", max_length=30)
    currency = models.CharField(max_length=30, default='still missing')
    capital = models.CharField(max_length=30, default='still missing')
    language = models.CharField(max_length=30, default='still missing')

    # Returns the string representation of the model.
    def __str__(self):
        return self.name   

class Data(models.Model):
    date = models.DateField()
    country = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True, default='nan')