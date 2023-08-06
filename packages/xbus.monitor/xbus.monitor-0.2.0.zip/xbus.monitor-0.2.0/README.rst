xbus.monitor
============

This package provides tools to monitor and administer Xbus <http://xbus.io>.

The monitor serves a REST API; it also includes a backbone.js client app:

- xbus_monitor_js <https://bitbucket.org/xcg/xbus_monitor_js>: Single-page
  JavaScript Backbone application that communicates with xbus.monitor via its
  REST API.


Xbus
----

Xbus is an Enterprise service bus. As such it aims to help IT departments
achieve a better application infrastructure layout by providing a way to
urbanize the IT systems.

The goals of urbanization are:

  - high coherence
  - low coupling

More information about Xbus:

  - Documentation: <http://xbusbroker.readthedocs.org/>
  - Website: <http://xbus.io/>
  - Presentation: <http://bit.ly/1AYtQa6>


Installing
----------

Set up a virtualenv::

    $ mkvirtualenv -p /usr/bin/python3 xbus

Install the xbus.monitor package::

    $ pip install xbus.monitor


Configuring
-----------

Follow the xbus.broker README file to set it up.

Xbus monitor settings are within the etc/production-example.ini file; grab it
from bitbucket (eg for the 0.1.2 version)::

    $ wget https://bitbucket.org/xcg/xbus.monitor/raw/0.1.2/etc/production-example.ini -O monitor.ini

Edit the file following comments written inside.

Localization:

    Edit the "pyramid.default_locale_name" variable. Note: Only "en_US" and
    "fr_FR" are supported for now.


Running
-------

Run as a regular Pyramid program::

  $ pserve monitor.ini


Run tests
---------

::

    nosetests

Development
-----------

When running the monitor for development purposes, it is recommended to deactivate the ``cookie.secure`` option in the configuration file::

    cookie.secure = false

Generate the translation template
---------------------------------

::

    pip install Babel lingua
    python setup.py extract_messages


Other translation tasks
-----------------------

See <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/i18n.html>.
::

    python setup.py [init_catalog -l en_US] [update_catalog] [compile_catalog]


Thanks
------

xbus.monitor uses the following external projects; thanks a lot to their respective authors:

    - pyramid <http://docs.pylonsproject.org/projects/pyramid/en/latest/>
    - pyramid_httpauth <https://github.com/tarzanjw/pyramid_httpauth>
