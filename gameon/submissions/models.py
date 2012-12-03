import micawber
from datetime import datetime
import string

from django.db import models
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import AnonymousUser
from django.conf import settings

from tower import ugettext_lazy as _

from gameon.users.models import Profile
from gameon.base.utils import _upload_path
from managers import ChallengeManager


class Challenge(models.Model):

    objects = ChallengeManager()

    name = models.CharField(max_length=200, verbose_name=(u'Challenge name'),
        unique=True)
    slug = models.SlugField(max_length=200, unique=True,
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
        return datetime.utcnow() > self.end_date


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_(u'Display name'),
        unique=True)
    slug = models.SlugField(max_length=100,
        unique=True, verbose_name=_(u'Slug'))
    description = models.TextField(verbose_name=_(u'Description'),
        blank=True)

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
        validators=[MaxLengthValidator(1000)], default="")
    category = models.ForeignKey(Category, verbose_name=_(u'Category'), blank=True,
        null=True)
    team_name = models.CharField(max_length=255, verbose_name=_(u'Team name'),
        blank=True)
    team_members = models.TextField(verbose_name=_(u'Members'),
        validators=[MaxLengthValidator(250)], blank=True)
    team_desciption = models.TextField(verbose_name=_(u'Description'),
        validators=[MaxLengthValidator(250)], blank=True)
    to_market = models.BooleanField(verbose_name="redirect to marketplace",
        default=False)

    def __unicode__(self):
        return self.title

    def editable_by(self, user=AnonymousUser()):
        if not user.is_anonymous():
            if self.created_by == user.get_profile():
                return True

    def get_image_src(self):
        """
        If a thumbnail has been included this provides an easy way to grab it
        from the DB and display it (or a default) in the templates
        """
        media_url = getattr(settings, 'MEDIA_URL', '')
        static_url = getattr(settings, 'STATIC_URL', '')
        path = lambda f: f and '%s%s' % (media_url, f)
        static_path = lambda f: f and '%s%s' % (static_url, f)
        return path(self.thumbnail) or static_path('base/img/entry-default.gif')

    @property
    def has_entry_feature(self):
        """
        If a project has provided a URL of gameplay action we want to display
        that in the single view template as the feature, opposed to the
        screenshot (which could still be the default)
        Only if the video is from a site that supported oembed do we class it as]
        'featurable'
        """
        return any(v in self.video_url for v in settings.ALLOWED_OMEMBED_SITES) or self.thumbnail

    def get_entry_feature(self):
        """
        If there is a video_url we want to include that as a feature, otherwise
        we fall through to the thumbnail
        """
        if self.video_url:
            """
            Ensure that the video is from a site that supports oembed
            """
            if any(v in self.video_url for v in settings.ALLOWED_OMEMBED_SITES):
                """
                Extracting the oembed data using https://github.com/coleifer/micawber
                """
                providers = micawber.bootstrap_basic()
                entry_oembed = micawber.parse_text(self.video_url, providers)
                """ Ensure https, less site warnings the better """
                return string.replace(entry_oembed, 'http://', 'https://')
        if self.thumbnail:
            return '<img src="%s" alt=""/>' % self.get_image_src()

    class Meta:
        verbose_name_plural = 'Entries'
