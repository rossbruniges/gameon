from django.shortcuts import render

import commonware

log = commonware.log.getLogger('playdoh')


def home(request, template='static_site/landing.html'):
    """Main example view."""
    data = {}  # You'd add data here that you're sending to the template.
    log.debug("I'm home!")
    return render(request, template, data)


def rules(request, template='static_site/rules.html'):
    """Main example view."""
    data = {}  # You'd add data here that you're sending to the template.
    log.debug("I'm reading the rules!")
    return render(request, template, data)


def judges(request, template='static_site/judges.html'):
    """Main example view."""
    data = {}  # You'd add data here that you're sending to the template.
    return render(request, template, data)


def prizes(request, template='static_site/prizes.html'):
    """Main example view."""
    data = {}  # You'd add data here that you're sending to the template.
    return render(request, template, data)


def resources(request, template='static_site/resources.html'):
    """Main example view."""
    data = {}  # You'd add data here that you're sending to the template.
    return render(request, template, data)


def previous(request, template='static_site/previous.html'):
    """Main example view."""
    data = {}  # You'd add data here that you're sending to the template.
    return render(request, template, data)


def categories(request, template='static_site/categories.html'):
    """Main example view."""
    data = {}  # You'd add data here that you're sending to the template.
    return render(request, template, data)
