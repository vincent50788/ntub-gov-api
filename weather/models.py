# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Weather(models.Model):
    locationname = models.CharField(max_length=15, blank=True, null=True)
    longitude = models.CharField(max_length=15, blank=True, null=True)
    latitude = models.CharField(max_length=15, blank=True, null=True)
    wind_dir = models.CharField(max_length=15, blank=True, null=True)
    wind_speed = models.CharField(max_length=15, blank=True, null=True)
    temp_now = models.CharField(max_length=15, blank=True, null=True)
    humd = models.CharField(max_length=15, blank=True, null=True)
    rainfall = models.CharField(max_length=15, blank=True, null=True)
    h_uvi = models.CharField(max_length=15, blank=True, null=True)
    temp_max = models.CharField(max_length=15, blank=True, null=True)
    tmax_time = models.CharField(max_length=15, blank=True, null=True)
    temp_min = models.CharField(max_length=15, blank=True, null=True)
    tmin_time = models.CharField(max_length=15, blank=True, null=True)
    uvi_status = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'weather'
