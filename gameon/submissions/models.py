from datetime import datetime

from django.db import models
from django.core.validators import MaxLengthValidator

from tower import ugettext_lazy as _

from gameon.users.models import Profile
from gameon.base.utils import _upload_path
from managers import ChallengeManager


class Challenge(models.Model):

    objects = ChallengeManager()

    name = models.CharField(max_length=200, verbose_name=(u'Challenge name'),
        unique=True)
    slug = models.SlugField(max_length=100, unique=True,
        verbose_name=_(u'Slug'))
    start_date = models.DateTimeField(verbose_name=_(u'Start date'))
    end_date = models.DateTimeField(verbose_name=_(u'End date'))

    def __unicode__(self):
        return self.name

    def has_started(self):
        return datetime.utcnow() > self.start_date

    def is_open(self):
        now = datetime.utcnow()
        return self.start_date < now and now < self.end_date

    def has_closed(self):
        return datetime.utcnow() < self.end_date


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_(u'Display name'),
        unique=True)
    slug = models.SlugField(max_length=100,
        unique=True, verbose_name=_(u'Slug'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Entry(models.Model):
    title = models.CharField(max_length=255, verbose_name=_(u'Entry title'),
        unique=True)
    slug = models.SlugField(max_length=255,
        unique=True, verbose_name=_(u'Slug'))
    url = models.URLField(verbose_name=_(u'URL'), max_length=255)
    thumbnail = models.ImageField(
        verbose_name=_(u'Featured image'), blank=True, null=True,
        help_text=_(u"This will be used in our summary and list views."),
        upload_to=_upload_path('submission-entry'))
    created_by = models.ForeignKey(Profile, blank=True, null=True)
    video_url = models.URLField(verbose_name=_(u'Gameplay URL'), max_length=255,
        default="")
    description = models.TextField(verbose_name=_(u'Description'),
        validators=[MaxLengthValidator(150)], default="")
    category = models.ForeignKey(Category, verbose_name=_(u'Category'), blank=True,
        null=True)
    team_name = models.CharField(max_length=255, verbose_name=_(u'Team name'),
        blank=True)
    team_members = models.TextField(verbose_name=_(u'Members'),
        validators=[MaxLengthValidator(300)], blank=True)
    team_desciption = models.TextField(verbose_name=_(u'Description'),
        validators=[MaxLengthValidator(200)], blank=True)
    to_market = models.BooleanField(verbose_name="redirect to marketplace",
        default=False)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Entries'
