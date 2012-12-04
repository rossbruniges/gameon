from django.db import models

from tower import ugettext_lazy as _
from datetime import datetime

from gameon.events.managers import EventManager


class Location(models.Model):
    name = models.CharField(max_length=255, verbose_name=(u'Location name'))
    street = models.CharField(max_length=255, verbose_name=(u'Street Address'))
    town = models.CharField(max_length=255, verbose_name=(u'Town'))
    country = models.CharField(max_length=255, verbose_name=(u'Country'))

    def __unicode__(self):
        return '%s - %s' % (self.name, self.country)


class Event(models.Model):

    objects = EventManager()

    name = models.CharField(max_length=255, verbose_name=(u'Event name'))
    url = models.URLField(verbose_name=_(u'Event URL'), max_length=255)
    location = models.ForeignKey(Location, blank=True, null=True)
    start_date = models.DateTimeField(verbose_name=_(u'Start date'))
    end_date = models.DateTimeField(verbose_name=_(u'End date'))

    def __unicode__(self):
        return self.name

    def has_finished(self):
        return datetime.utcnow() < self.end_date
