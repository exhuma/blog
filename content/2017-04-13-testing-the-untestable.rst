Testing the Untestable
######################

:date: 2017-04-13 07:52:20
:tags: python, unittesting, mocking, opensource
:category: programming

.. topic:: Abstract

    Sometimes you come across a code-base which has no unit-tests. This makes
    contributing to the project risky. If an application has not been written
    with unit-tests in mind from the beginning, it is often very difficult to
    add them later on. This article takes one such project and uses the
    fantastic ``unittest.mock`` Python module to add tests without modifying
    the code.


Preface
=======

From personal experience with old code-base maintainance, projects become hard
to unit-test for four main reasons:

* Violations of Demeter's Law.
* Fuzzy borders between the main application code and external I/O (like
  ``stdout``, databases, network services, ...).
* Hidden global state.
* Function-call side-effects / non-pure functions.

There are other reasons, but these are by far the ones I've ran across the
most.

.. note::

    The following article mentions the open-source project ``munin-influxdb``.
    It is *only* taken as illustrative example and I do not intend to paint
    this in a bad light.


As a starting point, we'll look at commit `8b6b4efca of munin-influxdb
<https://github.com/mvonthron/munin-influxdb/tree/8b6b4efcac22707c9c00675529e12e8d540e249a>`_.

THe project confronts us with several challenges:


Challenge 1 - No Clear  Entry-Point
===================================

The project contains a shell-script_ and separate modules in the ``bin`` subfolder.
Additionally, the ``setup.py`` module does not define any ``entry_points``

.. _shell-script: https://github.com/mvonthron/munin-influxdb/blob/8b6b4efcac22707c9c00675529e12e8d540e249a/muninflux

Issues
------

* As nothing is packaged probably it becomes non-trivial to install. Neither in
  an isolated virtual environment, nor on the system.
* Testing the main entry-point becomes more difficult as it is a bash script.

Solution
--------

Move the scripts from the ``bin`` folder into the project itself, and remove
the ``muninflux`` shell script. Use the argparse_ module to provide a
well-known "UI" to the end user. This has been achieved between commit
8b6b4efca_ and acea4515f_.

.. _acea4515f: https://github.com/exhuma/munin-influxdb/commit/acea4515fbee97cb95a400e0fa8b5e1239299871
.. _8b6b4efca: https://github.com/exhuma/munin-influxdb/commit/8b6b4efcac22707c9c00675529e12e8d540e249a

.. XXX TODO
.. _argparse: http://foo


Challenge 2 - Global State
==========================

In order to add unit-tests it is important that one can look at a piece (a
"unit") of code and can say what it's doing without looking through other parts
of the code. The project makes this difficult in it's current state. It makes
use of a ``Settings`` class containing key/value pairs which are populated at
run-time by various methods, and are not known in advance. If there's a
function taking a ``Settings`` instance as argument it's not trivial to "guess"
the structure of that instance to be able to run the function.

