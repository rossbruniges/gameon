from django.contrib import admin
from gameon.events import models


class EventAdmin(admin.ModelAdmin):
    model = models.Event
    list_display = ('name', 'location', 'start_date')

admin.site.register(models.Location)
admin.site.register(models.Event, EventAdmin)
