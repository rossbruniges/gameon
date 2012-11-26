from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required

from gameon.base.views import action_unavailable_response
from gameon.base.utils import get_page, get_paginator
from gameon.submissions.models import Entry, Category
from gameon.submissions.forms import EntryForm


@login_required
def create(request, template='submissions/create.html'):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.created_by = request.user.get_profile()
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
    return render(request, template, data)


def edit_entry(request, slug, template='submissions/edit.html'):
    entry = Entry.objects.get(slug=slug)
    if not entry.editable_by(request.user):
        return action_unavailable_response(request, case='no_edit_rights')
    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
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
                'form': form,
            }
    else:
        data = {
            'categories': Category.objects.all(),
            'form': EntryForm(instance=entry),
        }
    return render(request, template, data)


def list(request, category='all', template='submissions/list.html'):
    page_number = get_page(request.GET)
    if category == 'all':
        entry_set = Entry.objects.all().order_by('-pk')
        page_category = False
    else:
        entry_set = Entry.objects.filter(category__slug=category).order_by('-pk')
        page_category = Category.objects.get(slug=category)

    submissions = get_paginator(entry_set, page_number)

    data = {
        'submissions': submissions,
        'category': page_category,
        'categories': Category.objects.all(),
    }
    return render(request, template, data)


def single(request, slug, template='submissions/single.html'):
    data = {
        'entry': Entry.objects.get(slug=slug),
    }
    return render(request, template, data)
