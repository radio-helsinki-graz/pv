from django.db import models


class Master(models.Model):
    timestamp = models.BigIntegerField(primary_key=True)
    cart = models.IntegerField()
    len = models.IntegerField(null=True, blank=True)
    showtitle = models.CharField(max_length=765, blank=True)
    title = models.CharField(max_length=765, blank=True)
    artist = models.CharField(max_length=765, blank=True)
    album = models.CharField(max_length=765, blank=True)
    ismusic = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = u'master'
        ordering = ['-timestamp']


class Standby(models.Model):
    timestamp = models.BigIntegerField(primary_key=True)
    cart = models.IntegerField()
    len = models.IntegerField(null=True, blank=True)
    showtitle = models.CharField(max_length=765, blank=True)
    title = models.CharField(max_length=765, blank=True)
    artist = models.CharField(max_length=765, blank=True)
    album = models.CharField(max_length=765, blank=True)
    ismusic = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = u'standby'
        ordering = ['-timestamp']


class State(models.Model):
    timestamp = models.BigIntegerField(primary_key=True)
    state = models.CharField(max_length=96, blank=True)

    class Meta:
        db_table = u'state'
        ordering = ['-timestamp']
