Colorize Flask Logging
######################

:date: 2017-05-29 10:49:02
:tags: python, development
:category: programming

Here's a simple drop-in colorizer for Werkzeug (and thus also Flask) logs. It
won't make much sense in production, but makes development a bit more cheerful.

.. figure:: {filename}images/colorize_werkzeug.png
    :alt: Screenshot
    :target: |filename|/images/colorize_werkzeug.png

Adding `gouge.colourcli <https://pypi.python.org/pypi/gouge>`_ to the mix,
makes it even more colourful:

.. figure:: {filename}images/colorize_werkzeug2.png
    :alt: Screenshot using gouge.colourcli
    :target: |filename|/images/colorize_werkzeug2.png

To use it, simply put it in a utility module somewhere, import it and call
``colorize_wekzeug``.

You will need ``blessings``. If that's not available, the function will not do
any colorizing.

The code is hosted as a gist on GitHub:

[gist:id=81515c19eca1d4afaa57051a894b5c5d,file=colorize.py]
