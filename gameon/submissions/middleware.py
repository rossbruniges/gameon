from django.conf import settings
from gameon.submissions.models import Challenge


class ChallengeStatusMiddleware(object):

    def process_view(self, request, *args, **kwargs):
        """ Adds in the current challenge to request - so we know if it's open """
        if any(p in request.path for p in settings.MIDDLEWARE_URL_EXCEPTIONS):
            return
        request.challenge = Challenge.objects.get_current_challenge()
        return
