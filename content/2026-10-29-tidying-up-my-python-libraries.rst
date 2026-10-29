Tidying Up My Python Libraries
##############################

:date: 2026-10-29 18:00:00
:tags: python, opensource, x690, t61codec, gouge
:category: programming
:summary: Final releases for t61codec and config_resolver, a 2.0 for
          x690 and a refresh of gouge.

Last week I spent some time on my older Python libraries. t61codec,
x690, gouge and config_resolver all got a new release, and their docs
have moved to GitHub Pages.


t61codec 3.0.0
==============

t61codec_ is a Python codec for T.61 strings. You still run into those
in ASN.1 data, where they are called ``TeletexString``. Version 3.0.0
follows the 1988 version of the ITU-T spec to the letter. Accented
letters decode to precomposed characters, invalid input raises an error
instead of being guessed, and the incremental decoder copes with
sequences that are split across chunks.

The expected test data was written from the spec, *not* from the code.
I also compared the output with glibc's ``iconv`` over 1696 inputs. All
168 differences are intended and documented.

This is the last feature release. From now on it only gets fixes.


x690 2.0.0
==========

x690_ is the BER encoder and decoder behind puresnmp_. 2.0.0 is a
breaking release:

* It uses t61codec 3, so T.61 decoding is strict now.
* Context tags are registered per type instead of globally.
* More types decode to proper Python values (``str``, ``datetime``,
  ``float``).
* A decoded value can let go of the input it came from.

puresnmp and NXP's spsdk both pin ``x690 <2``, so they keep working
as before until they move to it.

It also got a lot faster. Reading items of a decoded sequence by index
was quadratic: 200 items took 40,200 header reads. Now it's at most
600. Decoding a file of 80 MB (on a Ryzen 5 5600X):

=========================  ===============  =============
Workload                   Before           After
=========================  ===============  =============
Full document              14.4 s / 232 MB  10.0 s / 8 MB
Last record only           2.2 s / 233 MB   0.71 s / 8 MB
10,000 records by index    167 s            10.5 s
=========================  ===============  =============

For whole documents, x690 is now the fastest of the five libraries I
benchmarked. pyasn1 needs 146 s and 9.5 GB for the same file. For
streaming, asn1crypto is still faster.


config_resolver 5.2.0
=====================

5.2.0 is the last release of config_resolver_. With the alternatives
around today, I don't see much value in keeping it.

It now emits a deprecation warning, and the docs have a migration page
with tested replacements: pydantic-settings for services,
``ConfigParser`` for existing INI files, and ``platformdirs`` with
``tomllib`` for CLI tools. The repository is archived.


gouge 2.3.0
===========

gouge_ fixes coloured tracebacks (some viewers lost the colour after
the first line) and adds JSON output and an option to show extra record
attributes, like a trace ID. The default output is byte-identical to
2.2.5, so existing setups don't change.


Docs and Python Support
=======================

The docs are now on GitHub Pages:

* https://exhuma.github.io/t61codec/
* https://exhuma.github.io/x690/
* https://exhuma.github.io/gouge/
* https://exhuma.github.io/config_resolver/

All four are tested against every supported CPython version, and
releases go out through PyPI's Trusted Publishing.

.. note::

    puresnmp still pins ``x690 <2``, so it doesn't use the new x690 yet.


.. _t61codec: https://github.com/exhuma/t61codec
.. _x690: https://github.com/exhuma/x690
.. _puresnmp: https://github.com/exhuma/puresnmp
.. _config_resolver: https://github.com/exhuma/config_resolver
.. _gouge: https://github.com/exhuma/gouge
