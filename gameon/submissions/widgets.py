from django.forms.widgets import RadioSelect, RadioFieldRenderer
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

from gameon.submissions.models import Category

from django.utils.html import escape, conditional_escape
from django.forms.widgets import ClearableFileInput, CheckboxInput


# The ClearableFieldWidget is pretty horrible - trying to make it a bit nicer
class AdvancedFileInput(ClearableFileInput):

    def __init__(self, *args, **kwargs):

        self.url_length = kwargs.pop('url_length', 30)
        self.preview = kwargs.pop('preview', True)
        self.image_width = kwargs.pop('image_width', 100)
        super(AdvancedFileInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None,):

        substitutions = {
            'initial_text': "<p class='meta'>Right now you have</p>",
            'input_text': '<span class="meta">Change this</span>',
            'clear_template': '',
            'clear_checkbox_label': '<span class="meta">Delete this</span>',
        }
        template = u'%(input)s'

        substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)

        if value and hasattr(value, "url"):

            template = self.template_with_initial
            if self.preview:
                substitutions['initial'] = (u'<span class="frame">\
                <img src="{0}" width="{2}"></span>'.format
                    (escape(value.url), '...' + escape(force_unicode(value))[-self.url_length:],
                     self.image_width))
            else:
                substitutions['initial'] = (u'<a href="{0}">{1}</a>'.format
                    (escape(value.url), '...' + escape(force_unicode(value))[-self.url_length:]))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)


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
