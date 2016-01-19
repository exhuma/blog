Alternative PostgreSQL plugin for munin |---| Part 2
####################################################

:date: 2015-11-10 08:00:49
:modified: 2015-11-27 14:01:34
:tags: munin, postgresql, python
:category: sysadmin



Related Posts
-------------

This post in part in a series:

`Part 1`_ |---| Part 2 (this post) |---| `Part 3`_ |---| `Part 4`_

.. _Part 1: {filename}2015-11-08-new-munin-postgresql-plugins.rst
.. _Part 3: {filename}2015-11-11-new-munin-postgresql-plugins-03.rst
.. _Part 4: {filename}2015-11-27-new-munin-postgresql-plugins-04.rst


First Alpha Releases
--------------------

I have finished porting all "virtual" graphs from the official plugins. The
source of this release can be found `on github`_.

This is currently a very rough cut release. Keep in mind:

* There is barely any documentation
* The plugin does not support ``autoconfig``
* It is likely that some major refactoring will go on once the docs are
  written.
* Maybe things will change. Maybe not.


Trying it out
-------------

Installation
~~~~~~~~~~~~

Installing the plugin is fairly easy:

* Clone the `github repository`_ somewhere and switch to the alpha tag::

    git clone https://github.com/exhuma/munin-plugins.git /opt/exhuma/munin-plugins
    cd /opt/exhuma/munin-plugins
    git checkout postgres-multigraph/v1.0.0a2

* Install ``psycopg2``::

    apt-get install python-psycopg2

* Symlink the plugin into your munin-node::

    ln -s /opt/exhuma/munin-plugins/pg_multigraph /etc/munin/plugins/pg_multigraph

.. _github repository: https://github.com/exhuma/munin-plugins.git

Configuration
~~~~~~~~~~~~~

The plugin reads the following environment variables:

PG_DBNAME (*default='template1'*)
    The database name to connect to.

PG_USER (*default='postgres'*)
    The username used to connect.

PG_PASSWORD (*default=''*)
    The password used to connect. If empty, perform a passwordless login.

PG_HOST (*default=''*)
    The DB host. If empty, connect using the unix domain socket.

PG_PORT (*default=0*)
    The port which is used to connect. If ``0``, connect using the unix domain socket.

PG_MULTIGRAPHS (*default='__all__'*)
    A comma-separated list of which graphs to create. At the time of this
    writing the following names are accepted:

    * ``__all__``
    * ``connections``
    * ``locks``
    * ``query_ages``
    * ``row_access``
    * ``scantypes``
    * ``sizes``
    * ``indexio``
    * ``sequenceio``
    * ``tableio``

    The special name ``__all__`` causes all graphs to be generated.



What's different?
-----------------

Compared to the plugins bundled with munin, there are a couple of differences
in the generated graphs:

* Locks show both "granted" and "waiting" locks. The official plugin did not
  differentiate between both.
* ``postgres_transactions_`` has not been ported. I have not use-case for that
  one.
* ``index scan`` and ``sequential scan`` is removed from ``tuple access``. It
  is now also related to ``row access``. Both scan fetches are more related to
  indices and pollute that graph.
* Buffer Cache has been removed and replaced by sepearate I/O plugins for
  Tables, Sequences and Indices.



Screenshots?
------------

I have currently no screenshots at hand which are really representative. All I
have is some "work in progress" stuff from my laptop. They don't represent the
graphs very well.


.. _on github: https://github.com/exhuma/munin-plugins/tree/postgres-multigraph/v1.0.0a2


.. |---| unicode:: U+2014  .. em dash, trimming surrounding whitespace
