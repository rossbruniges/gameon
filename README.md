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
    `> git clone --recursive git@github:{you}/gameon.git`
3. Set up a new [virtual environment][venv] (no, you really should):
    1. If you haven't already, install virtualenv[^1]:  
        `> pip install virtualenv`
    2. Make sure you're in the repo folder:  
        `> cd gameon`
    3. Create a virtual environment in the `venv` subfolder:  
        `> virtualenv venv`
    4. And activate it:  
        `> source venv/bin/activate`
4. Install required libraries:  
    `> pip install -r requirements/compiled.txt`
5. Create a database for gameon
6. Create local settings file, and update accordingly:  
    `> cp gameon/settings/local.py{-dist,}`
7. Sync your new database:  
    `> python manage.py syncdb`  
    `> python manage.py migrate`
8. Start up your development server:  
    `> python manage.py runserver`
9. Have a party


[^1]: If you already work with `virtualenvwrapper`, we'll assume you know the
appropriate steps for using that instead.

[gameon-repo]: https://github.com/mozilla/gameon
[venv]: http://pypi.python.org/pypi/virtualenv



License
-------

This software is licensed under the [New BSD License][BSD]. For more
information, read the file ``LICENSE``.

[BSD]: http://creativecommons.org/licenses/BSD/

