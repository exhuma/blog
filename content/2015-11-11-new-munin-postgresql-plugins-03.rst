Alternative PostgreSQL plugin for munin |---| Part 3
####################################################

:date: 2015-11-11 08:08:21
:tags: munin, postgresql, python
:category: sysadmin



Related Posts
-------------

This post in part in a series:

`Part 1`_ |---| `Part 2`_ |---| Part 3 (this post)


Comparison with the Official Plugins
------------------------------------

The most obvious difference you see at first is that it's only one single file
instead of multiple. At this time I'm still pondering to break it apart, but I
have a strong tendency to leave it as it is.

If you want to only enable some of the graphs, this can be done using the
``PG_MULTIGRAPHS`` environment variable. See `Part 2`_ for details on this.

The main aim of the work was to aggregate those plugins which generated too
many graphs. While they show aggregated values on the default munin overview,
these new graphs  will show a breakdown page once clicking on them.

Quick overview:

  ============================= ==============================
   Official Plugin               Name for new plugin
  ============================= ==============================
   ``postgres_bgwriter``         Not ported (good enough).
   ``postgres_checkpoints``      Not ported (good enough).
   ``postgres_xlog``             Not ported (good enough).
   ``postgres_transactions_``    Not ported (no use-case).
   ``postgres_cache_``           Replaced with:

                                 * ``indexio``
                                 * ``sequenceio``
                                 * ``tableio``

   ``postgres_connections_``     ``connections``
   ``postgres_connections_db``   Merged with ``connections``.
   ``postgres_users``            Merged with ``connections``
   ``postgres_locks_``           ``locks``
   ``postgres_querylength_``     ``query_ages``
   ``postgres_scans_``           ``scan_types``
   ``postgres_size_``            ``sizes``
   ``postgres_tuples_``          ``row_access``
  ============================= ==============================


Design Decisions
----------------

General
~~~~~~~

Most graph aggregations use stacked areas to display values. The idea behind
this is that you are usually interested in the total value. Using stacks gives
you a much better view of this. Overlapping lines are more useful to see
correlations between values.

Most aggregations show the sum of all the agregates. In the case of the query
ages, it shows the maximum of all the aggregates.


Replacing ``postgres_cache_`` with 3 new I/O Plugins
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While investigating, I discovered the following stats tables:

* pg_statio_user_tables_
* pg_statio_user_sequences_
* pg_statio_user_indexes_

They give a more fine-grained view on buffer I/O than pg_stat_database_ and
decided to split that one up.

Connections to the DB
~~~~~~~~~~~~~~~~~~~~~

This currently shows connections by user. It does *not* show connections per DB
(yet?). I currently have no pressing plans to include connections per DB. So I
will leave it as-is for the time being.


Locks
~~~~~

The official plugin combines both locks which are granted with locks which
aren't (somewhere someone's waiting for the release). Personally, I find it
more important to watch for waiting locks than for granted locks. For this
reason, this plugin now splits both lock types up, showing granted locks on one
side of the X-axis, and waiting locks on the other.

This still keeps all the information from the old graphs, but adds an
additional element to it.


Query Ages
~~~~~~~~~~

I decided to use "age" instead of "length" as, in the context of a graph, this
makes more sense. Maybe I was a bit too nitpicky here.

The official graph shows both query and transaction start. The transaction
start is currently not yet implemented in the new graph, but I will do so once
this blog-post is done.


Scan Types
~~~~~~~~~~

Nothing of importance to say here.


Sizes
~~~~~

Nothing of importance to say here.


Row Access
~~~~~~~~~~

Named *Tuple Access* in the official plugins. I renamed it as the statistics
table in PG also talks about "row access". So do the docs.


.. |---| unicode:: U+2014  .. em dash, trimming surrounding whitespace
.. _Part 1: {filename}2015-11-08-new-munin-postgresql-plugins.rst
.. _Part 2: {filename}2015-11-09-new-munin-postgresql-plugins-02.rst
.. _pg_statio_user_tables: http://www.postgresql.org/docs/9.2/static/monitoring-stats.html#PG-STATIO-ALL-TABLES-VIEW
.. _pg_statio_user_sequences: http://www.postgresql.org/docs/9.2/static/monitoring-stats.html#PG-STATIO-ALL-SEQUENCES-VIEW
.. _pg_statio_user_indexes: http://www.postgresql.org/docs/9.2/static/monitoring-stats.html#PG-STATIO-ALL-INDEXES-VIEW
.. _pg_stat_database: http://www.postgresql.org/docs/9.2/static/monitoring-stats.html#PG-STAT-DATABASE-VIEW
