Alternative PostgreSQL plugin for munin |---| Part 4
####################################################

:date: 2015-11-27 13:41:03
:tags: munin, postgresql, python
:category: sysadmin



Related Posts
-------------

This post in part in a series:

`Part 1`_ |---| `Part 2`_ |---| `Part 3`_ |---| Part 4 (this post)


No longer "alpha"
-----------------

After running the graphs for some time, I am happy with the result, and they
have replaced most of the old Postgres graphs at work.


Changes since v1.0.0a2
----------------------

**Added "transaction age" to query ages.**
    This value was simply missing.

**Disabled value scaling**
    This affects how values are displayed and causes less fractional values.

**Added POD-Style documentation**
    Munin graphs require POD documentation. It is readable with ``munin-doc``.

**Graph Labels/Info**
    Improved the labels and info fields of graphs.

**autoconf**
    The graph is not auto-detectable with autoconf.

**Moved to postgresql category**
    The former category was used for testing to keep the graphs better apart.
    Now that they are production-ready, this is no longer needed.

**Transaction Stats**
    Added graph of committed/rolled-back transactions.

**Fixed counters for query-ages**
    The value sometimes came out as NaN. This is now properly reported as ``0``.

**Added a breakdown of DB sizes**
    Opening the DB-Sizes graphs will now show a more detailed view, containing
    separate sizes for "main data", "indexes", "free-space-map", "visibility
    map" and "TOAST tables".

    The values here usually sum up to *less* than the raw DB-size value. The
    DB-size value counts the on-disk size of the database folder. This may
    contain other/temporary files. In extreme cases (catastrophic server
    failure), the temporary files may not get cleaned up. This should become
    visible in this graph.

**Row Access is now stacked**
    This should make the graph more readable.

**Added default warning/crtitical values for QueryAges**
    The default warning is 1 hour, the critical limit is set to 12 hours.

**Removed IDLE connections from query ages**
    This blew up the graph in case an application kept an open connection
    without active work.





.. |---| unicode:: U+2014  .. em dash, trimming surrounding whitespace
.. _Part 1: {filename}2015-11-08-new-munin-postgresql-plugins.rst
.. _Part 2: {filename}2015-11-09-new-munin-postgresql-plugins-02.rst
.. _Part 3: {filename}2015-11-11-new-munin-postgresql-plugins-03.rst
