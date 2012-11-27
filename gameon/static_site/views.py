from django.shortcuts import render

import commonware

from gameon.submissions.models import Category

log = commonware.log.getLogger('playdoh')


def home(request, template='static_site/landing.html'):
    """Main example view."""
    data = {}
    return render(request, template, data)


def rules(request, template='static_site/rules.html'):
    """Main example view."""
    categories = Category.objects.all()
    data = {
        'hackable': categories.get(slug='hackable-games'),
        'learning': categories.get(slug='learning-games'),
        'mobile': categories.get(slug='mobile-games'),
    }
    return render(request, template, data)


def judges(request, template='static_site/judges.html'):
    """Main example view."""
    data = {}
    return render(request, template, data)


def judging(request, template='static_site/judging.html'):
    """Main example view."""
    data = {}
    return render(request, template, data)


def prizes(request, template='static_site/prizes.html'):
    """Main example view."""
    data = {}
    return render(request, template, data)


def resources(request, template='static_site/resources.html'):
    """Main example view."""
    data = {}
    return render(request, template, data)


def legal(request, template='static_site/legal.html'):
    """Main example view."""
    data = {}  # You'd add data here that you're sending to the template.
    return render(request, template, data)
