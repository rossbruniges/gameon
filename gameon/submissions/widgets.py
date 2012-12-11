from django.forms.widgets import RadioSelect, RadioFieldRenderer
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

from gameon.submissions.models import Category


# Used to display the category description with each category in a RadioSelect widget
class CategorySelectRenderer(RadioFieldRenderer):
    """Mainly duplicated from django.forms.widgets
    A custom widget that allows us to render the standard list of radios with
    the addition of contextural content about each option in the list (pulled
    direct) from the category model
    """

    def render(self):
        """Outputs a <ul> for this set of radio fields."""
        row_list = []
        # not a generator but more readable
        for w in self:
            # extra attributes
            cat = Category.objects.filter(name=w.choice_label)[0]
            row_list.append(u'<li>%s <span class="meta">%s</span></li>' %
                                                (force_unicode(w),
                                                force_unicode(cat.description)))

        return mark_safe(u'<ul>\n%s\n</ul>' % u'\n'.join(row_list))


class CategorySelectWidget(RadioSelect):
    """Mainly duplicated from django.forms.widgets
Adds extra attributes to the markup"""
    renderer = CategorySelectRenderer
