from django.db import models
from datetime import datetime


class EventManager(models.Manager):

    def get_upcoming(self):
        return self.get_query_set().filter(end_date__gt=datetime.utcnow())
