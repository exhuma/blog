Python
======

.. TODO MySQL on Python 3

Birds-Eye View
--------------

 * Slow
 * Runs on all major platforms.
 * JIT Compiled (into bytecode).
 * Large community. #8 on TIOBE Index (Java on #2, PHP on #7). Based on result
   of March 2015
 * Strict Syntax (indentation matters)!
 * *Large* Standard Library
 * Global Interpreter Lock (the GIL)
 * PEP 8


Implementations
~~~~~~~~~~~~~~~

 * **CPython** (the default - *recommended*).
 * Jython (runs in Java VM).
 * IronPython (runs in dotNET CLR).
 * PyPy (fast).
 * Stackless (microthreads).


Duck Typing
~~~~~~~~~~~

    When I see a bird that walks like a duck and swims like a duck and quacks
    like a duck, I call that bird a duck.

         *-- James Whitcomb Riley*

+--------------------+--------------------+---------------------+
|                    | **Strong Binding** | **Weak Binding**    |
+--------------------+--------------------+---------------------+
| **Static Typing**  | Java, C#           | ?                   |
+--------------------+--------------------+---------------------+
| **Dynamic Typing** | Python, Ruby       | PHP, C              |
+--------------------+--------------------+---------------------+



Python 2 or 3
-------------

 * Starting from Python 3.3 it has become really usable (current version is 3.4
   with 3.5 on the horizon).
 * No new features are added to Python 2 (f.ex.: ``asyncio``).
 * Python 3 has much improved Unicode support. It puts the developer in control
   (and enforces that control).
 * Python 3 is even slower than Python 2 (at the moment).
 * Legacy platforms may only support Python 2.


Installation
------------

Linux
~~~~~

Python is available by default on most Unix platforms. From distribution to
distribution, the version packaged by default may either be Python 2 (Debian,
Red-Hat), or Python 3 (Arch). But even on systems with Python 2 as default,
Python 3 is usually available in the package repository.

Python 2 and 3 can both happily live on the same system without interfering
with each other.

Windows
~~~~~~~

Installation on Windows is as easy as downlading the installer and running it.


Syntax
------

 * Everything is an Object. Even functions.
 * Mutable vs. Immutable Objects
 * mutable Default arguments


Standard Library
----------------

csv
~~~

A module to easily read and write CSV files.

.. code::
    :language: python

    from csv import Reader
    reader = Reader('filename')
    for row in reader:
        print ' '.join(row)


cmd
~~~

A module to write interactive console applications.

.. code::
    :language: python

    from cmd impot Cmd
    class MyApp(Cmd):

        def do_hello(line):
            '''
            Prints out "Hello World"
            '''
            print('Hello World')

    if __name__ == '__main__':
        app = MyApp()
        MyApp.run()


json
~~~~

Easily read and write JSON documents.

.. code::
    :language: python

    from json import load, dump
    data = load(open('myfile.json'))

    dump('''{
        "key": "value"
    }''', open('filename', 'w'))



collections
~~~~~~~~~~~

Extension Modules
-----------------

SQLAlchemy
~~~~~~~~~~

Flask
~~~~~

xlrd
~~~~

Requests
~~~~~~~~

Click
~~~~~

Alembic
~~~~~~~

