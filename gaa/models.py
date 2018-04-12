from django.db import models
from django.contrib.auth.models import User

class Panchayat(models.Model):
    panchayat = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    taluka = models.CharField(max_length=200)
    stdofliving = models.CharField(max_length=200)
    health = models.CharField(max_length=200)
    education = models.CharField(max_length=200)
    hdi = models.CharField(max_length=200)

    def __str__(self):
        return self.panchayat

class RankedPanchayat(models.Model):
    panchayat = models.CharField(max_length=200)
    dev_index = models.CharField(max_length=200)
    rank = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.panchayat

class villageDetails(models.Model):
    panchayat = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    xcor = models.CharField(max_length=200)
    ycor = models.CharField(max_length=200)

    def __str__(self):
        return self.panchayat
