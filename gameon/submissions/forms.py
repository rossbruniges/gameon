from django import forms
from django.forms.models import ModelChoiceField
from django.forms.widgets import CheckboxSelectMultiple

from gameon.submissions.models import Entry, Category

MARKET_CHOICES = (('True', 'Yes, I want to submit by game to the marketplace'),
    ('False', "No, I don't want to submit my game to the marketplace"))

entry_widgets = {
    'to_market': forms.RadioSelect(choices=MARKET_CHOICES),
}


class EntryForm(forms.ModelForm):

    category = ModelChoiceField(queryset=Category.objects.all(),
        empty_label=None, widget=CheckboxSelectMultiple)

    class Meta:
        model = Entry
        fields = ('title', 'url', 'description', 'category', 'thumbnail',
            'video_url', 'team_name', 'team_members', 'team_desciption',
            'to_market')
        widgets = entry_widgets
