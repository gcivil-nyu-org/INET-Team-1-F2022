from django.db import models

# Create your models here.
class place(models.Model):
    DBA = models.CharField(max_length=100)
    BORO = models.CharField(max_length=100) 
    BUILDING = models.CharField(max_length=20)
    STERRT = models.CharField(max_length = 40)
    ZIPCODE = models.FloatField()
    PHONE = models.CharField(max_length=12)
    CUISION = models.CharField(max_length=20)
    LATITUDE = models.FloatField()
    LONGTITUDE = models.FloatField()
    