Remapping Keys in Windows
#########################

:date: 2016-01-19 09:10:43
:tags: windows
:category: desktop

After having been using Linux for over 20 years now, one of the few things I
really miss in Windows, is the "`Compose Key`_". It does exist, but until
today, I was never happy with the mapping. For ages I have this mapped on the
Caps Lock key. But under Windows this sometimes leads to a "stuck" caps lock.
I've tried different Compose Key applications on Windows, and they all had the
same problem.

I was looking for something like ``.Xmodmap`` on Windows, and today I found it.
You can rebind scan codes using the Windows Registry.

An example entry might be the following::

    Windows Registry Editor Version 5.00

    [HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Keyboard Layout]
    "Scancode Map"=hex:00,00,00,00,00,00,00,00,02,00,00,00,5c,e0,3a,00,00,00,00,00


This maps scan code ``3a 00`` (usually sent by the caps-lock key) to ``5c e0``
(usually sent by the right Windows button). So now pressing caps-lock is
interpreted as the right windows key by the OS. This one can be safely bound as
compose key as it's not a "sticky" key like caps-lock.

Refernces:

* `Disabling Caps Lock <http://www.howtogeek.com/howto/windows-vista/disable-caps-lock-key-in-windows-vista/>`_
* `Scan Codes (official MS site) <https://msdn.microsoft.com/en-us/library/aa299374(v=vs.60).aspx>`_
* `Scan Codes (unofficial listing) <https://www.win.tue.nl/~aeb/linux/kbd/scancodes-1.html>`_

.. _Compose Key: https://en.wikipedia.org/wiki/Compose_key
