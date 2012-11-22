var mgo = window.mgo || {};

mgo.formsets = function() {
    var init;
    init = function() {
        var formset = $('fieldset.team-details'),
            formset_first = formset.find('div.field')[0],
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
    };
    return {
        'init': init
    };
}();