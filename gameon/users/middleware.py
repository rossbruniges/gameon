from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponseRedirect
from django.conf import settings

from gameon.users.models import get_profile_safely


class ProfileMiddleware(object):
    """
    This middleware will redirect a user, once signed into the site via Persona
    to complete their profile, at which point they agree to the Mozilla Privacy
    Policy
    """
    @classmethod
    def safe_paths(cls):
        """
        Paths we don't need to redirect on - at this point they've either
        disagreed or are in the process of agreeing so it would infinite loop
        """
        return ('users_edit', 'django.views.static.serve', 'users_signout')

    def is_safe(self, path):
        """
        Checks the current request path is in the safe list above and if so
        ignores it and returns as normal
        """
        try:
            match = resolve(path)
            return match.url_name in self.__class__.safe_paths()
        except:
            return False

    def process_request(self, request):
        """
        if it's a request for the django debug toolbar AND we're in dev we can
        ignore - this check now only applies to when the site is in dev
        """
        if settings.DEBUG and '__debug__' in request.path:
            return
        if self.is_safe(request.path):
            return
        # remove the locale string - resolve won't work with it included
        path = u'/%s' % ('/'.join(request.path.split('/')[2:]),)
        if self.is_safe(path):
            return
        if request.user.is_authenticated():
            profile = get_profile_safely(request.user, True)
            if profile.has_chosen_identifier:
                return
            return HttpResponseRedirect(reverse('users_edit'))
