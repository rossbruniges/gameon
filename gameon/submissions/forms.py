from django import forms
from django.forms.models import ModelChoiceField

from gameon.submissions.widgets import CategorySelectWidget

from gameon.submissions.models import Entry, Category

MARKET_CHOICES = (('True', 'Yes, I want to submit by game to the marketplace (you will get forwarded to the Firefox Marketplace on submission)'),
    ('False', "No, I don't want to submit my game to the marketplace"))

entry_fields = ('title', 'url', 'description', 'category', 'thumbnail',
            'video_url', 'team_name', 'team_members', 'team_description',
            'to_market')

entry_widgets = {
    'url': forms.TextInput(attrs={'aria-describedby': 'info_url'}),
    'description': forms.Textarea(attrs={'aria-describedby': 'info_description',
        'data-maxlength': '1000'}),
    'video_url': forms.TextInput(attrs={'aria-describedby': 'info_video_url'}),
    'team_members': forms.Textarea(attrs={'aria-describedby': 'info_team_members',
        'data-maxlength': '250'}),
    'team_description': forms.Textarea(attrs={'aria-describedby': 'info_team_description',
        'data-maxlength': '250'}),
    'to_market': forms.RadioSelect(choices=MARKET_CHOICES),
}


class EntryForm(forms.ModelForm):

    category = ModelChoiceField(queryset=Category.objects.all(),
                                empty_label=None,
                                widget=CategorySelectWidget())

    class Meta:
        model = Entry
        fields = entry_fields
        widgets = entry_widgets


class NewEntryForm(EntryForm):
    """ We want all new submissions to agree to the rules before they can submit """
    terms_and_conditions = forms.BooleanField()

    class Meta:
        model = Entry
        fields = entry_fields + ('terms_and_conditions',)
        widgets = entry_widgets
