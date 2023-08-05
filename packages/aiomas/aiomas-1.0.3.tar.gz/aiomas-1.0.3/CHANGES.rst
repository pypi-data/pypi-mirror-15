Changelog
=========

1.0.3 – 2016-05-09
------------------

- [FIX] The function ``asyncio.ensure_future()`` called in
  ``aiomas.util.create_task()`` was introduced in Python 3.4.4 and is not
  available in Python 3.4.0–3.4.3 (which is, e.g., used on Ubuntu 14.04).
  There is now a fallback to ``asyncio.async()`` if ``asyncio.ensure_future()``
  is not available.


1.0.2 – 2016-05-04
------------------

- [CHANGE] ``aiomas.util.create_task()`` replaces ``aiomas.util.async()``.
  ``aiomas.util.async()`` is now deprecated and will be removed in aiomas 2 and
  when a new Python release no longer allows to use *async* as name.

- [NEW] Added developer documentation.


1.0.1 – 2016-04-22
------------------

- [BREAKING CHANGE] Renamed the ``async`` argument for ``Container.create()``
  and ``Container.shutdown()`` to ``as_coro``.  Realized to late that it will
  come to name clashes with the ``async`` keyword added to Python 3.5.
  I assume that no one really uses this project yet, thus I mark it as bug-fix
  relaese rather then bumping aiomas to v2.

You can find information about older versions in the `documentation
<https://aiomas.readthedocs.io/en/latest/development/changelog.html>`_.
