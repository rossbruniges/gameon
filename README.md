gameon 2012
===========

gameon was first run in 2010 by Mozilla Labs. In 2012 Mozilla hope to run the
challenge again, and this site will contain the details when we have them.

[See what happened when we first ran gameon][gameon-2012]


[gameon-2012]: https://gaming.mozillalabs.com/



Built using playdoh
-------------------

Mozilla's Playdoh is a web application template based on [Django][django].

Patches are welcome! Feel free to fork and contribute to this project on
[github][gh-playdoh].

Full [documentation][docs] is available as well.


[django]: http://www.djangoproject.com/
[gh-playdoh]: https://github.com/mozilla/playdoh
[docs]: http://playdoh.rtfd.org/



Installation
------------

1. Fork [the core gameon repository][gameon-repo]
2. Clone your new repo:  
    `git clone --recursive git@github:{you}/gameon.git`
3. Create a new virtual environment (if that's your thing)
4. Install required libraries:  
    `pip install -r requirements/compiled.txt`
5. Create a database for gameon
6. Create local settings file, and update accordingly:  
    `cp gameon/settings/local.py{-dist,}`
7. Sync your new database:  
    `python manage.py syncdb`
8. Start up your development server:  
    `python manage.py runserver`
9. Have a party


[gameon-repo]: https://github.com/mozilla/gameon



License
-------

This software is licensed under the [New BSD License][BSD]. For more
information, read the file ``LICENSE``.

[BSD]: http://creativecommons.org/licenses/BSD/

