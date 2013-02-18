from django.shortcuts import render
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required

from tower import ugettext as _

from gameon.base.views import action_unavailable_response
from gameon.base.utils import get_page, get_paginator, UnicodeWriter
from gameon.submissions.models import Entry, Category
from gameon.submissions.forms import EntryForm, NewEntryForm


@login_required
def create(request, template='submissions/create.html'):
    if not request.challenge.is_open():
        return action_unavailable_response(request, case='challenge_closed')
    if request.method == 'POST':
        form = NewEntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.created_by = request.user.get_profile()
            entry.slug = slugify(entry.title)
            form.save()
            if entry.to_market == True:
                return HttpResponseRedirect(settings.MARKETPLACE_URL)
            else:
                messages.success(request, _('<strong>Game submitted!</strong>'))
                return HttpResponseRedirect(reverse('submissions.entry_single',
                    kwargs={'slug': entry.slug}))
        else:
            data = {
                'categories': Category.objects.all(),
                'form': form
            }
    else:
        data = {
            'categories': Category.objects.all(),
            'form': NewEntryForm()
        }
    return render(request, template, data)


def edit_entry(request, slug, template='submissions/edit.html'):
    entry = Entry.objects.get(slug=slug)
    if not entry.editable_by(request.user):
        return action_unavailable_response(request, case='no_edit_rights')
    if not request.challenge.is_open():
        return action_unavailable_response(request, case='challenge_closed')
    if request.method == 'POST':
        form = EntryForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.slug = slugify(entry.title)
            form.save()
            if entry.to_market == True:
                return HttpResponseRedirect(settings.MARKETPLACE_URL)
            else:
                messages.success(request, _('<strong>Game edited!</strong>'))
                return HttpResponseRedirect(reverse('submissions.entry_single',
                    kwargs={'slug': slugify(entry.title)}))
        else:
            data = {
                'categories': Category.objects.all(),
                'form': form,
                'mode': 'edit',
            }
    else:
        data = {
            'categories': Category.objects.all(),
            'form': EntryForm(instance=entry),
            'mode': 'edit',
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
    # throwing a 404 is MUCH better than a 500 eh?
    try:
        entry = Entry.objects.get(slug=slug)
    except Entry.DoesNotExist:
        raise Http404

    data = {
        'entry': entry,
    }
    return render(request, template, data)


def export_csv(request, template='submissions/table.html'):
    if not request.user.is_staff:
        return action_unavailable_response(request, case='not_staff')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="gameon_entries.csv"'

    entry_set = Entry.objects.all().order_by('-pk')

    # using the custom Unicode writer so the view doesn't explode
    writer = UnicodeWriter(response)
    # Write out the header row
    writer.writerow([
        'GAME NAME',
        'CATEGORY',
        'GAME WEBSITE',
        'GAME DESCRIPTION',
        'GAME SUBMISSION URL',
        'GAME VIDEO URL',
        'SUBMITTED BY',
        'SUBMITTED BIO',
        'SUBMIT TO MARKETPLACE?'
    ])
    for e in entry_set:
        writer.writerow([
            e.title,
            e.category.name,
            e.url,
            e.description,
            e.get_absolute_url(),
            e.video_url,
            e.created_by.display_name,
            e.created_by.bio,
            str(e.to_market),
        ])

    return response
