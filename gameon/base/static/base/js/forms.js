var mgo = window.mgo || {};

mgo.formsets = function() {
    var drop_down_form, textarea_counters;
    textarea_counters = function() {
        $('textarea').each(function() {
            var current = $(this),
                options = {
                    'maxCharacterSize': current.attr('data-maxlength'),
                    'displayFormat': '#input of #max characters used',
                    'originalStyle': 'meta char-count',
                    'warningStyle': 'warning-style'
                };
                current.textareaCount(options);
        });
    };
    dropdown_form = function() {
        var formset = $('fieldset.team-details');
        if (formset.length) {
            var formset_first = formset.find('div.field')[0],
                closed_text = 'Submitting as part of a team? Tell us about it!',
                open_text = 'Close',
                trigger = $('<button class="trigger">' + closed_text + '</button>').appendTo(formset);

            formset.addClass('js_enabled');
            trigger.click(function() {
                if (trigger.hasClass('open')) {
                    trigger.removeClass('open');
                    formset.addClass('js_enabled');
                    trigger.text(closed_text);
                } else {
                    trigger.addClass('open');
                    formset.removeClass('js_enabled');
                    $(formset_first).focus();
                    trigger.text(open_text);
                }
                return false;
            });
        }
    };
    return {
        'textarea_counters': textarea_counters,
        'dropdown_form': dropdown_form
    };
}();

mgo.formsets.textarea_counters();
mgo.formsets.dropdown_form();