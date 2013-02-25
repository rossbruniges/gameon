from django.shortcuts import render

import commonware

from gameon.submissions.models import Category, Entry, Challenge
from gameon.events.models import Event


log = commonware.log.getLogger('playdoh')


def home(request, template='static_site/landing.html'):
    upcoming_events = Event.objects.get_upcoming()
    current_challenge = Challenge.objects.get_current_challenge()

    if not current_challenge.announce_winners:
        data = {
            'events': upcoming_events.order_by('start_date')[:5],
            'num_events': upcoming_events.count(),
        }
    else:
        data = {
            'winners': {
                'champ': Entry.objects.get(award="champ"),
                'best_hack': Entry.objects.get(award="best-hack"),
                'best_device': Entry.objects.get(award="best-device"),
                'best_web': Entry.objects.get(award="best-web"),
            }
        }
        template = 'static_site/closed.html'

    return render(request, template, data)


def rules(request, template='static_site/rules.html'):
    data = {
        'categories': Category.objects.all().order_by('name'),
    }
    return render(request, template, data)


def judges(request, template='static_site/judges.html'):
    data = {}
    return render(request, template, data)


def judging(request, template='static_site/judging.html'):
    data = {}
    return render(request, template, data)


def prizes(request, template='static_site/prizes.html'):
    data = {
        'categories': Category.objects.all().order_by('name'),
    }
    return render(request, template, data)


def resources(request, template='static_site/resources.html'):
    data = {}
    return render(request, template, data)


def legal(request, template='static_site/legal.html'):
    data = {}
    return render(request, template, data)


def faqs(request, template='static_site/faqs.html'):
    data = {}
    return render(request, template, data)
