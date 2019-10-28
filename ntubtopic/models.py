# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Alerts(models.Model):
    city = models.CharField(primary_key=True, max_length=5)
    hazard = models.CharField(max_length=5, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    longitude = models.CharField(max_length=5, blank=True, null=True)
    latitude = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alerts'


class AqiQuality(models.Model):
    site_id = models.AutoField(primary_key=True)
    sitename = models.CharField(max_length=5, blank=True, null=True)
    county = models.CharField(max_length=5, blank=True, null=True)
    aqi = models.CharField(max_length=5, blank=True, null=True)
    pollutant = models.CharField(max_length=5, blank=True, null=True)
    status = models.CharField(max_length=5, blank=True, null=True)
    pm10 = models.CharField(max_length=5, blank=True, null=True)
    pm25 = models.CharField(max_length=5, blank=True, null=True)
    wind_speed = models.CharField(max_length=5, blank=True, null=True)
    wind_dict = models.CharField(max_length=5, blank=True, null=True)
    pm10_avg = models.CharField(max_length=5, blank=True, null=True)
    pm25_avg = models.CharField(max_length=5, blank=True, null=True)
    longitude = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.CharField(max_length=10, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    pmtwo_status = models.CharField(max_length=5, blank=True, null=True)
    sotwo = models.CharField(max_length=5, blank=True, null=True)
    co = models.CharField(max_length=5, blank=True, null=True)
    othree = models.CharField(max_length=5, blank=True, null=True)
    sotwo_avg = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aqi_quality'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DangerousArea(models.Model):
    location = models.CharField(max_length=5, blank=True, null=True)
    longitude = models.CharField(max_length=5, blank=True, null=True)
    latitude = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dangerous_area'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Oils(models.Model):
    unleaded = models.CharField(max_length=5, blank=True, null=True)
    super = models.CharField(max_length=5, blank=True, null=True)
    supreme = models.CharField(max_length=5, blank=True, null=True)
    alcohol_gas = models.CharField(max_length=5, blank=True, null=True)
    diesel = models.CharField(max_length=5, blank=True, null=True)
    liquefied_gas = models.CharField(max_length=5, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oils'


class PreWeather(models.Model):
    city = models.CharField(primary_key=True, max_length=5)
    today_starttime = models.TimeField(blank=True, null=True)
    today_endtime = models.TimeField(blank=True, null=True)
    today_startdate = models.DateField(blank=True, null=True)
    today_enddate = models.DateField(blank=True, null=True)
    today_starttime_field = models.TimeField(db_column='today_starttime_', blank=True, null=True)  # Field renamed because it ended with '_'.
    today_endtime_field = models.TimeField(db_column='today_endtime_', blank=True, null=True)  # Field renamed because it ended with '_'.
    today_startdate_field = models.DateField(db_column='today_startdate_', blank=True, null=True)  # Field renamed because it ended with '_'.
    today_enddate_field = models.DateField(db_column='today_enddate_', blank=True, null=True)  # Field renamed because it ended with '_'.
    tomorrow_starttime = models.TimeField(blank=True, null=True)
    tomorrow_endtime = models.TimeField(blank=True, null=True)
    tomorrow_startdate = models.DateField(blank=True, null=True)
    tomorrow_enddate = models.DateField(blank=True, null=True)
    today_maxt = models.CharField(max_length=5, blank=True, null=True)
    today_maxt_field = models.CharField(db_column='today_maxt_', max_length=5, blank=True, null=True)  # Field renamed because it ended with '_'.
    tomorrow_maxt = models.CharField(max_length=5, blank=True, null=True)
    today_mint = models.CharField(max_length=5, blank=True, null=True)
    today_mint_field = models.CharField(db_column='today_mint_', max_length=5, blank=True, null=True)  # Field renamed because it ended with '_'.
    tomorrow_mint = models.CharField(max_length=5, blank=True, null=True)
    today_wx = models.CharField(max_length=5, blank=True, null=True)
    today_wx_field = models.CharField(db_column='today_wx_', max_length=5)  # Field renamed because it ended with '_'.
    tomorrow_wx = models.CharField(max_length=5, blank=True, null=True)
    today_pop = models.CharField(max_length=5, blank=True, null=True)
    today_pop_field = models.CharField(db_column='today_pop_', max_length=5, blank=True, null=True)  # Field renamed because it ended with '_'.
    tomorrow_pop = models.CharField(max_length=5, blank=True, null=True)
    longitude = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pre_weather'


class Weather(models.Model):
    locationname = models.CharField(max_length=5, blank=True, null=True)
    longitude = models.CharField(max_length=5, blank=True, null=True)
    latitude = models.CharField(max_length=5, blank=True, null=True)
    wind_dir = models.CharField(max_length=5, blank=True, null=True)
    wind_speed = models.CharField(max_length=5, blank=True, null=True)
    temp_now = models.CharField(max_length=5, blank=True, null=True)
    humd = models.CharField(max_length=5, blank=True, null=True)
    rainfall = models.CharField(max_length=5, blank=True, null=True)
    h_uvi = models.CharField(max_length=5, blank=True, null=True)
    temp_max = models.CharField(max_length=5, blank=True, null=True)
    tmax_time = models.CharField(max_length=5, blank=True, null=True)
    temp_min = models.CharField(max_length=5, blank=True, null=True)
    tmin_time = models.CharField(max_length=5, blank=True, null=True)
    uvi_status = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'weather'
