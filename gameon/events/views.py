from django.shortcuts import render

from gameon.events.models import Event


def list(request, template='events/list.html'):
    """
    Display a list of events - until we have this functionality on webmaker.org
    """
    return render(request, template, {
        'events': Event.objects.get_upcoming().order_by('start_date'),
    })
