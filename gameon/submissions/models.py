from datetime import datetime
import re

from django.db import models
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.conf import settings

from tower import ugettext_lazy as _

from gameon.users.models import Profile
from gameon.base.utils import _upload_path
from managers import ChallengeManager

URL_TO_EMBED_MAPPINGS = {
    # Embed code is taken from:
    # http://apiblog.youtube.com/2010/07/new-way-to-embed-youtube-videos.html
    'youtube': {
        'regexps': [
            re.compile(r'^https?://youtu\.be/(?P<VIDEO_ID>\w+)$'),
            re.compile(r'^https?://www.youtube.com/watch\?v=(?P<VIDEO_ID>\w+)$')
        ],
        'embed': """<iframe class="youtube-player" type="text/html" width="%(WIDTH)d" height="%(HEIGHT)d" src="https://www.youtube.com/embed/%(VIDEO_ID)s" frameborder="0"></iframe>"""
    },
    # Embed code obtained through inference/reverse-engineering. Not
    # ideal, but worst-case scenario means a blank iframe or none at all,
    # rather than e.g. an XSS attack.
    'vimeo': {
        'regexps': [
            re.compile(r'^https?://vimeo.com/.*?(?P<VIDEO_ID>[0-9]+)$')
        ],
        'embed': """<iframe src="https://player.vimeo.com/video/%(VIDEO_ID)s?title=0&amp;byline=0&amp;portrait=0&amp;badge=0" width="%(WIDTH)d" height="%(HEIGHT)d" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>"""
    }
}

AWARD_CHOICES = (
    ('best-hack', 'Best Hackable Game'),
    ('best-device', 'Best Multi-Device Game'),
    ('best-web', 'Best Web-Only Game'),
    ('notable', 'Notable Runner-Up')
)


def url2embed(url):
    if not url:
        return
    for service_name in URL_TO_EMBED_MAPPINGS:
        service = URL_TO_EMBED_MAPPINGS[service_name]
        for regexp in service['regexps']:
            result = regexp.match(url)
            if result:
                args = settings.VIDEO_EMBED_SETTINGS.copy()
                args.update(result.groupdict())
                return service['embed'] % args


class Challenge(models.Model):

    objects = ChallengeManager()

    name = models.CharField(max_length=200, verbose_name=(u'Challenge name'),
        unique=True)
    slug = models.SlugField(max_length=200, unique=True,
        verbose_name=_(u'Slug'))
    start_date = models.DateTimeField(verbose_name=_(u'Start date'))
    end_date = models.DateTimeField(verbose_name=_(u'End date'))
    announce_winners = models.BooleanField(default=False,
        help_text="Tick when you've selected the winners and want to tell people!")

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
    awarded_for = models.TextField(verbose_name=_(u'Awarded for'),
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
    team_description = models.TextField(verbose_name=_(u'Description'),
        validators=[MaxLengthValidator(250)], blank=True)
    to_market = models.BooleanField(verbose_name="redirect to marketplace",
        default=False)
    award = models.CharField(max_length=255, blank=True, null=True,
        choices=AWARD_CHOICES)
    is_grand_champ = models.BooleanField(default=False, blank=True)

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
        return url2embed(self.video_url) or self.thumbnail

    @property
    def has_award(self):
        return self.award or False

    def get_award_title(self):
        badge_values = filter(lambda x: x[0] == self.award, AWARD_CHOICES)[0]
        if self.is_grand_champ:
            return "Grand Champion and %s" % badge_values[1]
        else:
            return badge_values[1]

    def get_award_badge(self, check_champ=False):
        static_url = getattr(settings, 'STATIC_URL', '')
        static_path = lambda f: f and '%s%s' % (static_url, f)
        badge_values = filter(lambda x: x[0] == self.award, AWARD_CHOICES)[0]
        if check_champ and self.is_grand_champ:
            return '<img class="badge" src="%s" alt="This entry was awarded %s" />' % (
                static_path('base/img/badges/%s.png' % "champ"),
                "Grand Champion"
            )
        else:
            return '<img class="badge" src="%s" alt="This entry was awarded %s" />' % (
                static_path('base/img/badges/%s.png' % badge_values[0]),
                badge_values[1]
            )

    def get_entry_feature(self):
        """
        If there is a video_url we want to include that as a feature, otherwise
        we fall through to the thumbnail
        """
        video_embed = url2embed(self.video_url)
        if video_embed:
            return video_embed
        if self.thumbnail:
            return '<img src="%s" alt=""/>' % self.get_image_src()

    def get_absolute_url(self):
        site_url = getattr(settings, 'SITE_URL', '')
        entry_url = reverse('submissions.entry_single',
            kwargs={'slug': self.slug})

        return "%s%s" % (site_url, entry_url)

    class Meta:
        verbose_name_plural = 'Entries'
