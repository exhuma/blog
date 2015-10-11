How to write "nested" graphs for Munin
======================================


:date: 2015-10-11 10:58:21
:tags: munin, monitoring
:category: sysadmin


Preface
-------

To make this tutorial useful to an as wide audience as possible, I will begin
to explain the basics of Munin plugins first. If you are only interested in
nested graphs, feel free to directly jump to either the `Multigraphs`_ or
`Nested Graphs`_ section.

Terms Used
~~~~~~~~~~

dashboard
    The default view when opening the Munin web-interface. It shows daily and
    weekly graphs for each plugin.

year-view
    The view when clicking on a traditional graph. It shows daily, weekly,
    monthly and yearly graphs for the selected plugin.

breakdown
    The view when clicking on a *nested* graph. It shows daily and weekly
    graphs for each subgraph in the selected plugin.



Basics
------

I will try to show a comprehensive minimal example starting from a simple
plugin, but if you have not yet read `the tutorial on how to write plugins`_ [#]_,
you should.

I will *not* show any plugin source-code. But rather focus on the output that
Munin needs to see on stdout!

.. _the tutorial on how to write plugins: http://munin-monitoring.org/wiki/HowToWritePlugins
.. [#] At the time of this writing, the Munin documentation is undergoing a
       transition, but the plugin authoring document is still at it's old location!


Walkthrough
-----------


Essentials
~~~~~~~~~~


.. note:: You can skip this if you already know how to write simple plugins.

Let's start with a simple, basic plugin. At the very least you need to handle
two cases:

#. The plugin is called without arguments, and
#. The plugin is called with the argument ``config``.

Munin runs the plugin with the ``config`` argument to figure out what values to expect
and how to graph them (lines, areas, stacks, colours, labels, …).

The absolute minimum looks like this::

    $ /path/to/plugin config
    graph_title Really simple, static graph
    graph_vlabel Static value
    myvar.label Static value

This will create a graph named ``Really simple, static graph`` in the category
``other`` (the default). It will expect values for a variable named ``myvar``.
You can of course name it however you like.  For more configuration options,
look up `the official Munin documentation`_.

Next, now that Munin knows what variables to expect, it will get them by
calling the plugin without any arguments. It expects a line for each variable
with its value. In our case::

    $ /path/to/plugin
    myvar.value 10

This is all you need for a basic plugin. There is much more to know about
plugins. This is out of the scope of this tutorial. See the official
documentation for that.

Using the same code for multiple graphs (essentials #2)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes you can run the same core code for multiple graphs while only
changing one variable. A good example is the graph for network interface
statistics.  Traditionally, this is achieved by creating one core plugin, then
symlinking that with other names. This lets you use the basename of the
executable to determine the variable. Example:

**if_**
    This plugin on its own does nothing.

**if_eth0**
    Symlink to ``if_``. Accessing the basename and cutting off ``if_`` lets you
    determine that the stats are supposed to run for ``eth0``.

Now you can run the same code-base for multiple graphs.


Multigraphs
~~~~~~~~~~~

The above method to run multiple graphs has a few downsides:

* The whole plugin has to be executed for each variable. Even if it could
  technically share some data between executions. This can be wasteful if it's
  an expensive process.
* For each new created link, the munin-node needs to be restarted. It cannot be
  dynamically add/remove graphs.
* It potentially create a *lot* of graphs on the "dashboard". A good culprit
  for this are the PostgreSQL plugins. This easily creates more than 5 graphs
  per database, and can be painful to scroll through on a system with many DBs.


Multigraphs tackle these problems one way or another. The latter one is solved
by using "nested" graphs which we'll get to shortly.

The Munin documentation claims that multigraphs tend to be complex. While that
may be true for some cases, I personally find that they are still very easy to
write for basic needs.

To write a multigraph, the only thing you need, is preface each graph with the
``multigraph`` statement. Here's an example defining two graphs in one
``config`` command::

    $ /path/to/plugin config
    multigraph myfirstgraph
    graph_title Really simple, static graph
    graph_vlabel Static value
    myvar.label Static value

    multigraph mysecondgraph
    graph_title Another , static graph
    graph_vlabel Static value
    myvar.label Static value

This will generate two graphs named ``myfirstgraph`` and ``mysecondgraph``.
They are both *completely independent*! The big difference to classical plugins
is that they are generated by the same process. And can thus share expensive
resources.

Additionally, if the process generates more ``multigraph`` sections on
subsequent runs, new graphs will dynamically appear. Conversely, if existing
``multigraph`` section *disappears*, the corresponding graph(s) will disappear
as well!

.. warning::
    At the time of this writing, RRD files of graphs are *not* removed when a
    multigraph section disappears! So be careful not to fill up the disk with
    "temporary" graphs!

This is extremely useful for situations where graphs can appear/disappear
during the life-time of the monitored node. A good example is the
aforementioned PostgreSQL situation. With the classic plugins, you need to
create a new symlink and reload the node each time a new DB is created.

But how about the values? They are generated in the same way as the config::

    $ /path/to/plugin
    multigraph myfirstgraph
    myvar.value 10

    multigraph mysecondgraph
    myvar.value 20

Note that the variable names and values are *local* to the corresponding
``multigraph`` section of the config! In this example both ``myvar`` variables
are completely independent!


Nested Graphs
-------------


What are "nested" graphs?
~~~~~~~~~~~~~~~~~~~~~~~~~

The default Munin view (the "dashboard") shows you the day and week view of
each graph.

When clicking on one of those graphs, you will see an overview of the selected
plugin including the month and year. The "year-view".

A "nested" graph adds one additional "breakdown" step between the default and
"year-view" to this.


So instead of going::

    dashboard → year-view

You will go::

    dashboard → breakdown → year view


.. note::
    The values you report for the dashboard do not necessarily have to be
    related to the breakdown! While this might not seem to make sense at first
    sight, there may be some intersting applications for this. Just keep in
    mind that **you can report completely different values with a different
    config on the "dashboard" as on the "breakdown"!** An interesting exmple
    might be a dashboard graph reporting an arbitrry "I/O health" score based
    on inode usage, disk IOs and IOstat. Then on the breakdown, report each
    individual graph.


Writing Nested Graphs
~~~~~~~~~~~~~~~~~~~~~

Writing nested graphs is extremely easy, and build on `Multigraphs`_ and simply
uses names separated by dots. For example, if you have one "dashboard" graph
named ``summaryscore`` and two "breakdown" charts called ``diskscore`` and
``cpuscore``, the names shown in the multigraph config are:

* ``summaryscore``
* ``summaryscore.diskscore``
* ``summaryscore.cpuscore``

The config would look like this::

    $ /path/to/plugin config
    multigraph summaryscore
    graph_title Summery Health Score
    graph_vlabel Score (higher = better)
    health_summary.label Health Summary

    multigraph summaryscore.diskscore
    graph_title Disk score
    graph_vlabel Disk score (higher = better)
    temperature_score.label Temperature
    iowait_score.label IO Wait
    mtbf_score.label MTBF
    mtbf_score.info Days until MTBF

    multigraph summaryscore.cpuscore
    graph_title CPU score
    graph_vlabel CPU score (higher = better)
    temperature_score.label Temperature
    age_score.label Age
    age.info Age of the CPU


The corresponding values would look like this::

    $ /path/to/plugin
    multigraph summaryscore
    health_summary.value 98

    multigraph summaryscore.diskscore
    temperature_score.label 99
    iowait_score.label 99
    mtbf_score.label 65

    multigraph summaryscore.cpuscore
    temperature_score.label 87
    age_score.label 99


This would create only one graph ("Summary Health Score") on the dashboard. And
once you would click on it you would see the week-view of the two sub-graphs
"Disk Score" and "CPU Score".

How the values are determined is entirely up to you.

Now, the above example is extremely contrived, and I have no real-world
example. But it should get the point across.

Hope this helped and made writing Munin plugins easier.

Happy coding!

.. _the official Munin documentation: http://munin-monitoring.org/wiki/HowToWritePlugins
