Changelog
=========


0.2.0 (2016-06-27)
------------------

  - Add new consumer event type settings (related to optional data lookup" /
    clearing features).

  - Resolve aiozmq endpoints beforehand.

  - Safer consumer getter.

  - Log Xbus requests by default in the example configuration file.

  - Simplified deployment; this application now includes a default client.

  - Reworked the login system to apply on the whole client app instead of
    triggering on specific JS requests.

  - Adapt to message tracking changes done in xbus.broker.


0.1.4 (2015-05-25)
------------------

  - Event types: Allow setting the "immediate reply" flag.

  - Update requirements.


0.1.3 (2015-05-18)
------------------

  - Define required package versions in setup.py and document why some are
    frozen.


0.1.2 Initial release (2015-05-12)
----------------------------------

  - Initial implementation of the Xbus monitor.
