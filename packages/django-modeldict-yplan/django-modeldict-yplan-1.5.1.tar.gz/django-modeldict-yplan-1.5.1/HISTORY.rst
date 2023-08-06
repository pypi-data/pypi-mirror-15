.. :changelog:

=======
History
=======

Pending release
---------------

* New release notes here

1.5.1 (2016-06-13)
------------------

* Fixed local cache never expiring if value was checked too often.
* Use Django's ``cache.set_many`` for more efficient storage.

1.5.0 (2016-01-11)
------------------

* Forked by YPlan
* Fixed concurrency TOCTTOU bug for threaded Django servers.
* Stopped including the 'tests' directory in package
* Django 1.8 and 1.9 supported.
* Python 3 support added.
* Fixed ``setdefault()`` to return the value that was set/found, as per normal dict semantics. Thanks @olevinsky.

1.4.1 (2012-12-04)
------------------

* Last release by Disqus
