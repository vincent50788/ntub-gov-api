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
    sitename = models.CharField(max_length=5, blank=True, null=True)
    county = models.CharField(max_length=5, blank=True, null=True)
    aqi = models.IntegerField(blank=True, null=True)
    pollutant = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    pm10 = models.IntegerField(blank=True, null=True)
    pm25 = models.IntegerField(blank=True, null=True)
    wind_speed = models.FloatField(blank=True, null=True)
    wind_dict = models.FloatField(blank=True, null=True)
    pm10_avg = models.IntegerField(blank=True, null=True)
    pm25_avg = models.IntegerField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aqi_quality'



