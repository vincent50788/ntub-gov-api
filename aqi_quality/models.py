# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AqiQuality(models.Model):
    site_id = models.AutoField(primary_key=True)
    sitename = models.CharField(max_length=10, blank=True, null=True)
    county = models.CharField(max_length=10, blank=True, null=True)
    aqi = models.CharField(max_length=10, blank=True, null=True)
    pollutant = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    pm10 = models.CharField(max_length=10, blank=True, null=True)
    pm25 = models.CharField(max_length=10, blank=True, null=True)
    wind_speed = models.CharField(max_length=10, blank=True, null=True)
    wind_dict = models.CharField(max_length=10, blank=True, null=True)
    pm10_avg = models.CharField(max_length=10, blank=True, null=True)
    pm25_avg = models.CharField(max_length=10, blank=True, null=True)
    longitude = models.CharField(max_length=15, blank=True, null=True)
    latitude = models.CharField(max_length=15, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    pmtwo_status = models.CharField(max_length=10, blank=True, null=True)
    sotwo = models.CharField(max_length=10, blank=True, null=True)
    co = models.CharField(max_length=10, blank=True, null=True)
    othree = models.CharField(max_length=10, blank=True, null=True)
    sotwo_avg = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aqi_quality'
