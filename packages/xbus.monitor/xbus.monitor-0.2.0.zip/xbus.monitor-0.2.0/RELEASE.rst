How to release
==============

First make sure everything is good and all tests are passing.
Then make sure you are working on the correct monitor_js by
using ensureconf::

  hg ensureconf


If you want to know which version of monitorjs you are using just
check in .hgconf

When everything is fine just::

  python setup.py release


Verify and test your release. ie: open the source dist to make sure
it contains all it should...

If something is missing from the source dist, edit MANIFEST.in to include
it.

When you are happy with the results and you tested a pip install an a test
machine to ensure all works properly::

  python setup.py release_upload

When this is done IMMEDIATELY tag using the version number ACTUALLY present in
your setup.py file. example: if version=0.7.3 in setup.py::

  hg tag 0.7.3

Then and only then! Edit setup.py and bump to a higher version. Don't be
afraid, this version number will be labeled .dev1 as long a you only
setup.py develop. If you want to know why look into setup.cfg

BTW: in order to release you should upload a PGP key id to pypi because we
added the sign argument to the upload method.

And last but not least::

  hg push

So that the central repository receives your new tags and development version.
