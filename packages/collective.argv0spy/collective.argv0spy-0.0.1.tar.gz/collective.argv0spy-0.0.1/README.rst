.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide_addons.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
collective.argv0spy
==============================================================================

This package manipulates the process title to show the urls your threads are currently serving.

It is quite simplistic, it does not show you for how long it is working on the request and it will not show idle threads as idle.

This gives you information when running ps or top, these tools show the up to date process name.

See it in action::

    $ ps auxwwww | grep zope.conf | grep -v grep
    do3cc           48824  83.5  1.0  2634876 159628 s004  R+   12:17AM   0:14.15 /Users/do3cc/.dev/collective.argv0spy/bin/python2.7 /Users/do3cc/dev/collective.argv0spy/parts/instance/bin/interpreter /Users/do3cc/dev/collective.argv0spy/eggs/Zope2-2.13.24-py2.7.egg/Zope2/Startup/run.py -C /Users/do3cc/dev/collective.argv0spy/parts/instance/etc/zope.conf -X debug-mode=on /Plone/less-variables.js /Plone/less-variables.js /Plone/less-variables.js /Plone/less-variables.js /Plone/less-variables.js

You see 5 times the request for the Resource /Plone/less-variables.js, A resource a chose by random and hammered my Zope instance with ab.
Interesting Tidbit: This is a standard Plone instance, it runs with 4 threads but you see 5 requests here. This happens because we log Requests when they get received from the main thread, that does not count as one of the four zserver-threads. Think of it as the queue.

Features
--------

- shows url in the process name.


Documentation
-------------

This is the full documentation

Installation
------------

Install collective.arg0spy  by adding it to your buildout::

   [buildout]

    ...

    eggs =
        collective.argv0spy
    zcml =
        collective.argv0spy


and then running "bin/buildout"
You do not need to activate your plugin. The plugin will be active for all Plone instances of your zope process.

Nothing gets installed in the Database, so removing the pcakge from your buildout and rerunning buildout will remove this package without leaving a trace.


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.argv0spy/issues
- Source Code: https://github.com/collective/collective.argv0spy
- Documentation: https://github.com/collective/collective.argv0spy

License
-------

This package is MIT licensed
