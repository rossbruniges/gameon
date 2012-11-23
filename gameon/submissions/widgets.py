from django.forms.widgets import RadioSelect, RadioFieldRenderer
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from gameon.submissions.models import Category


class CustomRadioFieldRenderer(RadioFieldRenderer):
    """Mainly duplicated from django.forms.widgets
Adds extra supporting info to each field"""

    def render(self):
        """Outputs a <ul> for this set of radio fields."""
        row_list = []
        # not a generator but more readable
        for w in self:
            # extra attributes
            cat = Category.objects.filter(name=w.choice_label)[0]
            cat_url = reverse('submissions.entry_list', args=(cat.slug,))
            row_list.append(u'<li>%s <span class="meta">%s <a href="%s" target="_blank">Like these ones</a>.</span></li>' %
                                                (force_unicode(w),
                                                force_unicode(cat.description),
                                                 cat_url))

        return mark_safe(u'<ul>\n%s\n</ul>' % u'\n'.join(row_list))


class CustomRadioSelect(RadioSelect):
    """Mainly duplicated from django.forms.widgets
Adds extra attributes to the markup"""
    renderer = CustomRadioFieldRenderer
