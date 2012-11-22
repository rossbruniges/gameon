import commonware

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify

from gameon.submissions.models import Entry, Category
from gameon.submissions.forms import EntryForm

log = commonware.log.getLogger('playdoh')


def create(request, template='submissions/create.html'):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.slug = slugify(entry.title)
            form.save()
            if entry.to_market == True:
                return HttpResponseRedirect(settings.MARKETPLACE_URL)
            else:
                return HttpResponseRedirect(reverse('submissions.entry_list',
                    kwargs={'category': 'all'}))
        else:
            data = {
                'categories': Category.objects.all(),
                'form': form
            }
    else:
        data = {
            'categories': Category.objects.all(),
            'form': EntryForm()
        }
    log.debug("Single submission page")
    return render(request, template, data)


def list(request, category='all', template='submissions/list.html'):
    if category == 'all':
        submissions = Entry.objects.all()
    else:
        submissions = Entry.objects.filter(category__slug=category)
    data = {
        'submissions': submissions,
        'category': category
    }  # You'd add data here that you're sending to the template.
    log.debug("List view of all submissions")
    return render(request, template, data)


def single(request, slug, template='submissions/single.html'):
    data = {
        'entry': Entry.objects.get(slug=slug)
    }  # You'd add data here that you're sending to the template.
    log.debug("Single ")
    return render(request, template, data)
