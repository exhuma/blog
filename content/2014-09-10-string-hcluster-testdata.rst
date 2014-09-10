Validating the test-case for clustering string values
=====================================================

:date: 2014-09-10 12:43:40
:tags: algorithms, github, python
:category: programming

Here we go again...

After further analysis (the trial & error kind), I found out that the error of
modified values only occurs in unsorted data. Which makes perfect sense as
Python's ``list.remove`` picks the *first matching item*. So the ordering of
data plays a role.

As a quick fix, sorted data is now enforced when using the hierarchical
clustering algorithm. Now, the only remaining test failure is the one comparing
string values. And this time, I'll prepare a *real* test-case!

Which means manually calculating the matrix and clusters. So here we go!

The input data (lorem-ipsum split on white-space)::

    ['Lorem', 'ipsum', 'dolor', 'sit', 'amet,', 'consectetuer', 'adipiscing',
     'elit.', 'Ut', 'elit.', 'Phasellus', 'consequat', 'ultricies', 'mi.',
     'Sed', 'congue', 'leo', 'at', 'neque.', 'Nullam.']

As distance function, we'll use Python's SequenceMatcher_.

.. _SequenceMatcher: https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher.ratio

2h30m later
-----------

Funnily enough, the matrices are now generated using another quick-and-dirty
script. With this input data, doing it manually was a bit too much after all.
However, this time, the resulting values look actually correct!

This new algorithm is completely written from scratch, and could possibly
replace the existing algorithm in the library.  But I have other ideas for that
one, so I'll leave it for now...

And indeed, fixing the above mentioned "sorting" issue fixes the problem.
Running the tests with the new test-data, against the old code checks out.

There was one discrepancy though: On the final iteration of the test (going
from matrix #10 to matrix #11) there are several candidates with a distance of
``0.600``. And the code which generated the test matrices below picked ``(leo,
dolor), Lorem`` where the original algorithm picked ``adipiscing, ipsum``. Both
values are correct, so the result of the test is indeed valid!


Matrices
--------

.. csv-table:: Matrix #1
    :header-rows: 1
    :stub-columns: 1
    :delim: :

    :Lorem: ipsum: dolor: sit: amet: consectetuer: adipiscing: elit: Ut: elit: Phasellus: consequat: ultricies: mi: Sed: congue: leo: at: neque: Nullam
    Lorem: 
    ipsum: 0.800
    dolor: 0.600: 1.000
    sit: 1.000: 0.750: 1.000
    amet: 0.778: 0.778: 1.000: 0.714
    consectetuer: 0.765: 0.765: 0.765: 0.733: 0.750
    adipiscing: 1.000: 0.600: 0.867: 0.846: 0.857: 0.818
    elit: 0.778: 0.778: 0.778: 0.429: 0.500: 0.750: 0.857
    Ut: 1.000: 1.000: 1.000: 0.600: 0.667: 0.857: 1.000: 0.667
    elit: 0.778: 0.778: 0.778: 0.429: 0.500: 0.750: 0.857: 0.000: 0.667
    Phasellus: 0.857: 0.714: 0.857: 0.833: 0.692: 0.714: 0.789: 0.692: 1.000: 0.692
    consequat: 0.714: 0.714: 0.857: 0.667: 0.692: 0.429: 0.789: 0.692: 0.818: 0.692: 0.667
    ultricies: 0.714: 0.857: 0.714: 0.833: 0.846: 0.810: 0.684: 0.692: 0.818: 0.692: 0.778: 0.778
    mi: 0.714: 0.714: 1.000: 0.600: 0.667: 1.000: 0.833: 0.667: 1.000: 0.667: 1.000: 1.000: 0.818
    Sed: 0.750: 1.000: 0.750: 1.000: 0.714: 0.867: 0.846: 0.714: 1.000: 0.714: 0.833: 0.833: 0.833: 1.000
    congue: 0.636: 0.818: 0.818: 1.000: 0.800: 0.444: 0.625: 0.800: 1.000: 0.800: 0.867: 0.467: 0.733: 1.000: 0.778
    leo: 0.750: 1.000: 0.500: 1.000: 0.714: 0.867: 1.000: 0.714: 1.000: 0.714: 0.833: 0.833: 0.667: 1.000: 0.667: 0.778
    at: 1.000: 1.000: 1.000: 0.600: 0.333: 0.857: 0.833: 0.667: 0.500: 0.667: 0.818: 0.636: 0.818: 1.000: 1.000: 1.000: 1.000
    neque: 0.800: 0.800: 1.000: 1.000: 0.778: 0.529: 0.867: 0.778: 1.000: 0.778: 0.714: 0.429: 0.857: 1.000: 0.750: 0.455: 0.750: 1.000
    Nullam: 0.818: 0.636: 0.818: 1.000: 0.600: 0.889: 0.875: 0.800: 1.000: 0.800: 0.733: 0.733: 0.733: 0.750: 1.000: 0.833: 0.778: 0.750: 0.818


.. csv-table:: Matrix #2
    :header-rows: 1
    :stub-columns: 1
    :delim: :

    :Lorem: ipsum: dolor: sit: amet: consectetuer: adipiscing: Ut: Phasellus: consequat: ultricies: mi: Sed: congue: leo: at: neque: Nullam: elit, elit
    Lorem: 
    ipsum: 0.800
    dolor: 0.600: 1.000
    sit: 1.000: 0.750: 1.000
    amet: 0.778: 0.778: 1.000: 0.714
    consectetuer: 0.765: 0.765: 0.765: 0.733: 0.750
    adipiscing: 1.000: 0.600: 0.867: 0.846: 0.857: 0.818
    Ut: 1.000: 1.000: 1.000: 0.600: 0.667: 0.857: 1.000
    Phasellus: 0.857: 0.714: 0.857: 0.833: 0.692: 0.714: 0.789: 1.000
    consequat: 0.714: 0.714: 0.857: 0.667: 0.692: 0.429: 0.789: 0.818: 0.667
    ultricies: 0.714: 0.857: 0.714: 0.833: 0.846: 0.810: 0.684: 0.818: 0.778: 0.778
    mi: 0.714: 0.714: 1.000: 0.600: 0.667: 1.000: 0.833: 1.000: 1.000: 1.000: 0.818
    Sed: 0.750: 1.000: 0.750: 1.000: 0.714: 0.867: 0.846: 1.000: 0.833: 0.833: 0.833: 1.000
    congue: 0.636: 0.818: 0.818: 1.000: 0.800: 0.444: 0.625: 1.000: 0.867: 0.467: 0.733: 1.000: 0.778
    leo: 0.750: 1.000: 0.500: 1.000: 0.714: 0.867: 1.000: 1.000: 0.833: 0.833: 0.667: 1.000: 0.667: 0.778
    at: 1.000: 1.000: 1.000: 0.600: 0.333: 0.857: 0.833: 0.500: 0.818: 0.636: 0.818: 1.000: 1.000: 1.000: 1.000
    neque: 0.800: 0.800: 1.000: 1.000: 0.778: 0.529: 0.867: 1.000: 0.714: 0.429: 0.857: 1.000: 0.750: 0.455: 0.750: 1.000
    Nullam: 0.818: 0.636: 0.818: 1.000: 0.600: 0.889: 0.875: 1.000: 0.733: 0.733: 0.733: 0.750: 1.000: 0.833: 0.778: 0.750: 0.818
    elit,elit: 0.778: 0.778: 0.778: 0.429: 0.500: 0.750: 0.857: 0.667: 0.692: 0.692: 0.846: 0.667: 0.714: 0.800: 0.714: 0.667: 0.778: 0.800


.. csv-table:: Matrix #3
    :header-rows: 1
    :stub-columns: 1
    :delim: :

    :Lorem: ipsum: dolor: sit: consectetuer: adipiscing: Ut: Phasellus: consequat: ultricies: mi: Sed: congue: leo: neque: Nullam: elit, elit: at, amet
    Lorem: 
    ipsum: 0.800
    dolor: 0.600: 1.000
    sit: 1.000: 0.750: 1.000
    consectetuer: 0.765: 0.765: 0.765: 0.733
    adipiscing: 1.000: 0.600: 0.867: 0.846: 0.818
    Ut: 1.000: 1.000: 1.000: 0.600: 0.857: 1.000
    Phasellus: 0.857: 0.714: 0.857: 0.833: 0.714: 0.789: 1.000
    consequat: 0.714: 0.714: 0.857: 0.667: 0.429: 0.789: 0.818: 0.667
    ultricies: 0.714: 0.857: 0.714: 0.833: 0.810: 0.684: 0.818: 0.778: 0.778
    mi: 0.714: 0.714: 1.000: 0.600: 1.000: 0.833: 1.000: 1.000: 1.000: 0.818
    Sed: 0.750: 1.000: 0.750: 1.000: 0.867: 0.846: 1.000: 0.833: 0.833: 0.833: 1.000
    congue: 0.636: 0.818: 0.818: 1.000: 0.444: 0.625: 1.000: 0.867: 0.467: 0.733: 1.000: 0.778
    leo: 0.750: 1.000: 0.500: 1.000: 0.867: 1.000: 1.000: 0.833: 0.833: 0.667: 1.000: 0.667: 0.778
    neque: 0.800: 0.800: 1.000: 1.000: 0.529: 0.867: 1.000: 0.714: 0.429: 0.857: 1.000: 0.750: 0.455: 0.750
    Nullam: 0.818: 0.636: 0.818: 1.000: 0.889: 0.875: 1.000: 0.733: 0.733: 0.733: 0.750: 1.000: 0.833: 0.778: 0.818
    elit,elit: 0.778: 0.778: 0.778: 0.429: 0.750: 0.857: 0.667: 0.692: 0.692: 0.846: 0.667: 0.714: 0.800: 0.714: 0.778: 0.800
    at,amet: 0.778: 0.778: 1.000: 0.600: 0.750: 0.833: 0.500: 0.692: 0.636: 0.818: 0.667: 0.714: 0.800: 0.714: 0.778: 0.600: 0.500


.. csv-table:: Matrix #4
    :header-rows: 1
    :stub-columns: 1
    :delim: :

    :Lorem: ipsum: dolor: sit: adipiscing: Ut: Phasellus: ultricies: mi: Sed: congue: leo: neque: Nullam: elit, elit: at, amet: consequat, consectetuer
    Lorem: 
    ipsum: 0.800
    dolor: 0.600: 1.000
    sit: 1.000: 0.750: 1.000
    adipiscing: 1.000: 0.600: 0.867: 0.846
    Ut: 1.000: 1.000: 1.000: 0.600: 1.000
    Phasellus: 0.857: 0.714: 0.857: 0.833: 0.789: 1.000
    ultricies: 0.714: 0.857: 0.714: 0.833: 0.684: 0.818: 0.778
    mi: 0.714: 0.714: 1.000: 0.600: 0.833: 1.000: 1.000: 0.818
    Sed: 0.750: 1.000: 0.750: 1.000: 0.846: 1.000: 0.833: 0.833: 1.000
    congue: 0.636: 0.818: 0.818: 1.000: 0.625: 1.000: 0.867: 0.733: 1.000: 0.778
    leo: 0.750: 1.000: 0.500: 1.000: 1.000: 1.000: 0.833: 0.667: 1.000: 0.667: 0.778
    neque: 0.800: 0.800: 1.000: 1.000: 0.867: 1.000: 0.714: 0.857: 1.000: 0.750: 0.455: 0.750
    Nullam: 0.818: 0.636: 0.818: 1.000: 0.875: 1.000: 0.733: 0.733: 0.750: 1.000: 0.833: 0.778: 0.818
    elit,elit: 0.778: 0.778: 0.778: 0.429: 0.857: 0.667: 0.692: 0.846: 0.667: 0.714: 0.800: 0.714: 0.778: 0.800
    at,amet: 0.778: 0.778: 1.000: 0.600: 0.833: 0.500: 0.692: 0.818: 0.667: 0.714: 0.800: 0.714: 0.778: 0.600: 0.500
    consequat,consectetuer: 0.714: 0.714: 0.765: 0.667: 0.789: 0.818: 0.667: 0.778: 1.000: 0.833: 0.444: 0.833: 0.429: 0.733: 0.692: 0.636


.. csv-table:: Matrix #5
    :header-rows: 1
    :stub-columns: 1
    :delim: :

    :Lorem: ipsum: dolor: adipiscing: Ut: Phasellus: ultricies: mi: Sed: congue: leo: neque: Nullam: at, amet: consequat, consectetuer: elit, elit, sit
    Lorem: 
    ipsum: 0.800
    dolor: 0.600: 1.000
    adipiscing: 1.000: 0.600: 0.867
    Ut: 1.000: 1.000: 1.000: 1.000
    Phasellus: 0.857: 0.714: 0.857: 0.789: 1.000
    ultricies: 0.714: 0.857: 0.714: 0.684: 0.818: 0.778
    mi: 0.714: 0.714: 1.000: 0.833: 1.000: 1.000: 0.818
    Sed: 0.750: 1.000: 0.750: 0.846: 1.000: 0.833: 0.833: 1.000
    congue: 0.636: 0.818: 0.818: 0.625: 1.000: 0.867: 0.733: 1.000: 0.778
    leo: 0.750: 1.000: 0.500: 1.000: 1.000: 0.833: 0.667: 1.000: 0.667: 0.778
    neque: 0.800: 0.800: 1.000: 0.867: 1.000: 0.714: 0.857: 1.000: 0.750: 0.455: 0.750
    Nullam: 0.818: 0.636: 0.818: 0.875: 1.000: 0.733: 0.733: 0.750: 1.000: 0.833: 0.778: 0.818
    at,amet: 0.778: 0.778: 1.000: 0.833: 0.500: 0.692: 0.818: 0.667: 0.714: 0.800: 0.714: 0.778: 0.600
    consequat,consectetuer: 0.714: 0.714: 0.765: 0.789: 0.818: 0.667: 0.778: 1.000: 0.833: 0.444: 0.833: 0.429: 0.733: 0.636
    elit,elit,sit: 0.778: 0.750: 0.778: 0.692: 0.600: 0.692: 0.833: 0.600: 0.714: 0.800: 0.714: 0.778: 0.800: 0.500: 0.667


.. csv-table:: Matrix #6
    :header-rows: 1
    :stub-columns: 1
    :delim: :

    :Lorem: ipsum: dolor: adipiscing: Ut: Phasellus: ultricies: mi: Sed: congue: leo: Nullam: at, amet: elit, elit, sit: consequat, consectetuer, neque
    Lorem: 
    ipsum: 0.800
    dolor: 0.600: 1.000
    adipiscing: 1.000: 0.600: 0.867
    Ut: 1.000: 1.000: 1.000: 1.000
    Phasellus: 0.857: 0.714: 0.857: 0.789: 1.000
    ultricies: 0.714: 0.857: 0.714: 0.684: 0.818: 0.778
    mi: 0.714: 0.714: 1.000: 0.833: 1.000: 1.000: 0.818
    Sed: 0.750: 1.000: 0.750: 0.846: 1.000: 0.833: 0.833: 1.000
    congue: 0.636: 0.818: 0.818: 0.625: 1.000: 0.867: 0.733: 1.000: 0.778
    leo: 0.750: 1.000: 0.500: 1.000: 1.000: 0.833: 0.667: 1.000: 0.667: 0.778
    Nullam: 0.818: 0.636: 0.818: 0.875: 1.000: 0.733: 0.733: 0.750: 1.000: 0.833: 0.778
    at,amet: 0.778: 0.778: 1.000: 0.833: 0.500: 0.692: 0.818: 0.667: 0.714: 0.800: 0.714: 0.600
    elit,elit,sit: 0.778: 0.750: 0.778: 0.692: 0.600: 0.692: 0.833: 0.600: 0.714: 0.800: 0.714: 0.800: 0.500
    consequat,consectetuer,neque: 0.714: 0.714: 0.765: 0.789: 0.818: 0.667: 0.778: 1.000: 0.750: 0.444: 0.750: 0.733: 0.636: 0.667


.. csv-table:: Matrix #7
    :header-rows: 1
    :stub-columns: 1
    :delim: :

    :Lorem: ipsum: dolor: adipiscing: Ut: Phasellus: ultricies: mi: Sed: leo: Nullam: at, amet: elit, elit, sit: consequat, consectetuer, neque, congue
    Lorem: 
    ipsum: 0.800
    dolor: 0.600: 1.000
    adipiscing: 1.000: 0.600: 0.867
    Ut: 1.000: 1.000: 1.000: 1.000
    Phasellus: 0.857: 0.714: 0.857: 0.789: 1.000
    ultricies: 0.714: 0.857: 0.714: 0.684: 0.818: 0.778
    mi: 0.714: 0.714: 1.000: 0.833: 1.000: 1.000: 0.818
    Sed: 0.750: 1.000: 0.750: 0.846: 1.000: 0.833: 0.833: 1.000
    leo: 0.750: 1.000: 0.500: 1.000: 1.000: 0.833: 0.667: 1.000: 0.667
    Nullam: 0.818: 0.636: 0.818: 0.875: 1.000: 0.733: 0.733: 0.750: 1.000: 0.778
    at,amet: 0.778: 0.778: 1.000: 0.833: 0.500: 0.692: 0.818: 0.667: 0.714: 0.714: 0.600
    elit,elit,sit: 0.778: 0.750: 0.778: 0.692: 0.600: 0.692: 0.833: 0.600: 0.714: 0.714: 0.800: 0.500
    consequat,consectetuer,neque,congue: 0.636: 0.714: 0.765: 0.625: 0.818: 0.667: 0.733: 1.000: 0.750: 0.750: 0.733: 0.636: 0.667


.. csv-table:: Matrix #8
    :header-rows: 1
    :stub-columns: 1
    :delim: :

    :Lorem: ipsum: adipiscing: Ut: Phasellus: ultricies: mi: Sed: Nullam: at, amet: elit, elit, sit: consequat, consectetuer, neque, congue: leo, dolor
    Lorem: 
    ipsum: 0.800
    adipiscing: 1.000: 0.600
    Ut: 1.000: 1.000: 1.000
    Phasellus: 0.857: 0.714: 0.789: 1.000
    ultricies: 0.714: 0.857: 0.684: 0.818: 0.778
    mi: 0.714: 0.714: 0.833: 1.000: 1.000: 0.818
    Sed: 0.750: 1.000: 0.846: 1.000: 0.833: 0.833: 1.000
    Nullam: 0.818: 0.636: 0.875: 1.000: 0.733: 0.733: 0.750: 1.000
    at,amet: 0.778: 0.778: 0.833: 0.500: 0.692: 0.818: 0.667: 0.714: 0.600
    elit,elit,sit: 0.778: 0.750: 0.692: 0.600: 0.692: 0.833: 0.600: 0.714: 0.800: 0.500
    consequat,consectetuer,neque,congue: 0.636: 0.714: 0.625: 0.818: 0.667: 0.733: 1.000: 0.750: 0.733: 0.636: 0.667
    leo,dolor: 0.600: 1.000: 0.867: 1.000: 0.833: 0.667: 1.000: 0.667: 0.778: 0.714: 0.714: 0.750


.. csv-table:: Matrix #9
    :header-rows: 1
    :stub-columns: 1
    :delim: :

    :Lorem: ipsum: adipiscing: Phasellus: ultricies: mi: Sed: Nullam: elit, elit, sit: consequat, consectetuer, neque, congue: leo, dolor: at, amet, Ut
    Lorem: 
    ipsum: 0.800
    adipiscing: 1.000: 0.600
    Phasellus: 0.857: 0.714: 0.789
    ultricies: 0.714: 0.857: 0.684: 0.778
    mi: 0.714: 0.714: 0.833: 1.000: 0.818
    Sed: 0.750: 1.000: 0.846: 0.833: 0.833: 1.000
    Nullam: 0.818: 0.636: 0.875: 0.733: 0.733: 0.750: 1.000
    elit,elit,sit: 0.778: 0.750: 0.692: 0.692: 0.833: 0.600: 0.714: 0.800
    consequat,consectetuer,neque,congue: 0.636: 0.714: 0.625: 0.667: 0.733: 1.000: 0.750: 0.733: 0.667
    leo,dolor: 0.600: 1.000: 0.867: 0.833: 0.667: 1.000: 0.667: 0.778: 0.714: 0.750
    at,amet,Ut: 0.778: 0.778: 0.833: 0.692: 0.818: 0.667: 0.714: 0.600: 0.500: 0.636: 0.714


.. csv-table:: Matrix #10
    :header-rows: 1
    :stub-columns: 1
    :delim: :

    :Lorem: ipsum: adipiscing: Phasellus: ultricies: mi: Sed: Nullam: consequat, consectetuer, neque, congue: leo, dolor: at, amet, Ut, elit, elit, sit
    Lorem: 
    ipsum: 0.800
    adipiscing: 1.000: 0.600
    Phasellus: 0.857: 0.714: 0.789
    ultricies: 0.714: 0.857: 0.684: 0.778
    mi: 0.714: 0.714: 0.833: 1.000: 0.818
    Sed: 0.750: 1.000: 0.846: 0.833: 0.833: 1.000
    Nullam: 0.818: 0.636: 0.875: 0.733: 0.733: 0.750: 1.000
    consequat,consectetuer,neque,congue: 0.636: 0.714: 0.625: 0.667: 0.733: 1.000: 0.750: 0.733
    leo,dolor: 0.600: 1.000: 0.867: 0.833: 0.667: 1.000: 0.667: 0.778: 0.750
    at,amet,Ut,elit,elit,sit: 0.778: 0.750: 0.692: 0.692: 0.818: 0.600: 0.714: 0.600: 0.636: 0.714


.. csv-table:: Matrix #11
    :header-rows: 1
    :stub-columns: 1
    :delim: :

    :Lorem: Phasellus: ultricies: mi: Sed: Nullam: consequat, consectetuer, neque, congue: leo, dolor: at, amet, Ut, elit, elit, sit: adipiscing, ipsum
    Lorem: 
    Phasellus: 0.857
    ultricies: 0.714: 0.778
    mi: 0.714: 1.000: 0.818
    Sed: 0.750: 0.833: 0.833: 1.000
    Nullam: 0.818: 0.733: 0.733: 0.750: 1.000
    consequat,consectetuer,neque,congue: 0.636: 0.667: 0.733: 1.000: 0.750: 0.733
    leo,dolor: 0.600: 0.833: 0.667: 1.000: 0.667: 0.778: 0.750
    at,amet,Ut,elit,elit,sit: 0.778: 0.692: 0.818: 0.600: 0.714: 0.600: 0.636: 0.714
    adipiscing,ipsum: 0.800: 0.714: 0.684: 0.714: 0.846: 0.636: 0.625: 0.867: 0.750


The remaining matrices have been left out, as this last one is the one we want for our unit-test!
