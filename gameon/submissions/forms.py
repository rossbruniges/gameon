from django import forms

from gameon.submissions.models import Entry


class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = ('title', 'url', 'description', 'category')
