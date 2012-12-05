var mgo = window.mgo || {};

mgo.pages = function() {
    var init;
    /*
        the included browserID JS file requires an anchor with an ID to bind
        functionality to. Super simple piggy back to allow for multiple
        personaID login buttons on the same page that don't rely on needing an
        ID to work
    */
    init = function() {
        var master_trigger = $('#browserid');
        if (master_trigger.length) {
            $('a.additional_persona').each(function(){
                $(this).click(function(){
                    master_trigger.click();
                    return false;
                });
            });
        }
        /*
            Due to CSP inline JS is a no-no, so I'm going to have to ditch my lovely
            piece of inlineJS that immediately (and without a library) removes the
            non-JS class and plonk it in here
        */
        $('html').removeClass('no-js');
    };
    return {
        'init': init
    };
}();

mgo.pages.init();