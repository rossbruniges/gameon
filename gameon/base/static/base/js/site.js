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
        if (master_trigger) {
            $('a.additional_persona').each(function(){
                $(this).click(function(){
                    master_trigger.click();
                    return false;
                });
            });
        }
    };
    return {
        'init': init
    };
}();

mgo.pages.init();