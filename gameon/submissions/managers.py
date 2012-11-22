from django.db import models
from django.conf import settings


class ChallengeManager(models.Manager):

    def get_current_challenge(self):
        """ Returns the challenge object we define in settings as being current """
        try:
            return self.get(slug=settings.GAMEON_CHALLENGE_SLUG)
        except self.model.DoesNotExist:
            return None
