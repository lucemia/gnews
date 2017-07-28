from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Channel(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name


class Stat(models.Model):
    channel = models.ForeignKey(Channel)
    date = models.DateField()

    recommend = models.IntegerField(default=0)
    read = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s-%s" % (self.channel, self.date)

    class Meta:
        unique_together = (('channel', 'date'), )
