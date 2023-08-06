devpi-server: pypi server for caching and private indexes
=============================================================================

* `issue tracker <https://bitbucket.org/hpk42/devpi/issues>`_, `repo
  <https://bitbucket.org/hpk42/devpi>`_

* IRC: #devpi on freenode, `mailing list
  <https://groups.google.com/d/forum/devpi-dev>`_ 

* compatibility: {win,unix}-py{26,27,34}

consistent robust pypi-cache
----------------------------------------

You can point ``pip or easy_install`` to the ``root/pypi/+simple/``
index, serving as a self-updating transparent cache for pypi-hosted
**and** external packages.  Cache-invalidation uses the latest and
greatest PyPI protocols.  The cache index continues to serve when
offline and will resume cache-updates once network is available.

user specific indexes
---------------------

Each user (which can represent a person or a project, team) can have
multiple indexes and upload packages and docs via standard ``setup.py``
invocations command.  Users and indexes can be manipulated through a
RESTful HTTP API.

index inheritance
--------------------------

Each index can be configured to merge in other indexes so that it serves
both its uploads and all releases from other index(es).  For example, an
index using ``root/pypi`` as a parent is a good place to test out a
release candidate before you push it to PyPI.

good defaults and easy deployment
---------------------------------------

Get started easily and create a permanent devpi-server deployment
including pre-configured templates for ``nginx`` and cron. 

separate tool for Packaging/Testing activities
-------------------------------------------------------

The complimentary `devpi-client <http://pypi.python.org/devpi-client>`_ tool
helps to manage users, indexes, logins and typical setup.py-based upload and
installation workflows.

See http://doc.devpi.net for getting started and documentation.



Changelog
=========

4.0.0 (2016-05-12)
------------------

.. note::

  Please note that devpi-server 4.0.0 is a bug fix/compatibility release as it
  only changes project name normalization compared to 3.1.x. The internal use
  of the normalization requires an export/import cycle, which is the reason for
  the major version increase. There are no other big changes and so everyone
  who used devpi-server 3.x.y should be fine just using 4.0.0. It's also fine
  to export from 2.6.x and import with 4.0.0.

- require devpi-common 3.0.0 which changes the normalization of project names.

- allow import of exported data from devpi-server 3.1.2 with inconsistently
  normalized project names.


3.1.2 (2016-05-12)
------------------

- fix issue336: the mirror_whitelist setting got lost on import.

- allow export if a package with dotted name was uploaded while
  devpi-common 2.0.9 was installed. The resulting export will only be
  importable with devpi-server 4.x. It will fail to import in 3.x with a
  MissingRegistration error.


3.1.1 (2016-05-11)
------------------

- fix import of releases for packages with dots in their name after PEP-503
  fix in devpi-common 2.0.9.


3.1.0 (2016-04-22)
------------------

- fix issue208: Uncached mirrored files (PyPI) are streamed to the client while
  downloading. This prevents timeouts in pip etc. The files are only cached if
  there were no errors and in case there is a checksum, the content matches.
  Downloads on replicas won't wait until they are in sync, but pass on what
  they get from the master.

- fix issue229: A replica talking to a master behind nginx decoded gzipped
  data, but left the Content-Encoding header unchanged. Now data is passed on
  unchanged.
  Thanks to Chad Wagner for the fix.

- fix issue317: When there is no data in the directory specified via
  ``--serverdir`` during export, then the process aborts instead of creating
  and exporting an empty database.

- fix issue210: When an external user authenticated by a plugin tries to create
  an index the required user object is now created automatically if the
  permissions allow it.

- address issue267: We unconditionally clean up the transaction if there was an
  exception in rollback or commit. This prevents issues in logging and a
  possible server lockup if at some point all threads contain a failed
  transaction object.

- fix issue321: All exceptions in the replica and event processing threads are
  caught now and can't stop the threads anymore.

- fix issue338: Handle trailing slash in project listing for mirror indexes.

- Added checks on the index dependency tree built from bases during import.

- Every project is now imported together with all it's release files on it's
  own serial. Before the release files each got their own serial. This reduces
  the number of serials generated, especially when there are many projects and
  releases. That in turn improves import, as well as replication and event
  handling times (in particular devpi-web indexing).


3.0.2 (2016-03-03)
------------------

- fix setting of ``mirror_whitelist``.

- normalize names when setting ``mirror_whitelist``.

- fix handling of 404 in mirror indexes on replicas.

- include version in file paths in exported data to avoid possible
  name conflicts.



