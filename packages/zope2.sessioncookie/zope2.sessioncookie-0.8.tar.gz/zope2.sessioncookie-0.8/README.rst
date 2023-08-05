``zope2.sessioncookie``
=============================

Bridge to allow using Pyramid's `cookie session implementation
<http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/sessions.html>`_
in Zope2.

.. note::

   Initial development of this library was sponsored by ZeOmega Inc.

Installation
------------

1. Clone the repository.  E.g.::

    $ cd /path/to/
    $ git clone git@github.com:zopefoundation/zope2.sessioncookie

2. Get ``zope2.sessioncookie`` installed on the Python path.  E.g.::

    $ cd /path/to/zope2.sessioncookie
    $ /path/to/virtualenv_with_zope2/bin/pip install -e .
    ...

3. Copy / link the ``zope2.sessioncookie-meta.zcml`` file into the
   ``$INSTANCE_HOME/etc/package-includes`` of your Zope instance.  (You might
   need to create the directory first.)  E.g.::

    $ cd /path/to/zopes_instance
    $ mkdir -p etc/package-includes
    $ cd etc/package-includes
    $ ln -s \
        /path/to/zope2.sessioncookie/zope2.sessioncookie-meta.zcml .

4. Generate a 32-byte, hexlified secret::

    $ /path/to/virtualenv_with_zope2/bin/print_secret
    DEADBEEFDEADBEEFDEADBEEFDEADBEEFDEADBEEFDEADBEEFDEADBEEFDEADBEEF

4. Edit the ``site.zcml`` for your instance.  E.g.::

    $ cd /path/to/zopes_instance
    $ vim etc/site.zcml

   Add an XML namespace declaration at the top, e.g.::
   
    xmlns:sc="https://github.com/zopefoundation/zope2.sessioncookie"

   Add a stanza near the end, configuring the cookie session.  E.g.::

    <sc:sessioncookie
     secret="DEADBEEFDEADBEEFDEADBEEFDEADBEEFDEADBEEFDEADBEEFDEADBEEFDEADBEEF"
     secure="False"
     encrypt="True"/>

5. Run the installation script, which disables the standard session
   manager and adds the new hook.  E.g.::

    $ bin/zopectl run \
        /path/to/zope2.sessioncookie/zope2/sessioncookie/scripts/install.py

6. (Re)start your Zope instance.  Test methods which set session variables,
   and inspect request / response cookies to see that ``_ZopeId`` is no longer
   being set, while ``session`` *is* set (with encrypted, base64-encoded data).
