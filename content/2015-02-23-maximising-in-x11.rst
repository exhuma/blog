Maximising xterm and gvim in KDE
################################

:date: 2015-02-23 10:52:15
:tags: kde, linux, desktop
:category: desktop

The Problem
-----------

For ages, I was annoyed that neither ``gvim`` nor ``xterm`` maximised properly
in some desktop environment (KDE being one of them). They both have a small
"gap" around the outermost screen edges. It is not only visually annoying, but
I am also used to "throw" the mouse to the top corner to grab the title-bar.
But because this small gap exists, I always end up clicking anything which lies
behind that window.

.. figure:: {filename}images/x11-fullscreen/fullscreen-1-2.png
    :alt: Visual gap between the screen edges and the application window.
    :figwidth: 300px
    :align: left
    :target: |filename|/images/x11-fullscreen/fullscreen-1-2.png

    Note the visual gap between the application and the window on it's left.
    gvim (or xterm) is maximised, and the other window is sitting on a second
    monitor. The gap is clearly visible.

The reason this happens, is because the applications give the window
manager resizing hints. And because both applications are resized based on
characters, and *not* based on pixels, the WM tries it's best to fill as much
screen as possible. But only changing the size by the increments given by the
application. This depends on font and font-size. It is unlikely that the width
and height of the characters can perfectly fill the screen.

.. raw:: html

    <br clear="both" />


Solution
--------

KDE offers you a way to ignore those hints.

.. figure:: {filename}images/x11-fullscreen/fullscreen-3.png
    :alt: Context menu for the application.
    :figwidth: 300px
    :align: left
    :target: |filename|/images/x11-fullscreen/fullscreen-3.png

    The context menu for special application settings.

When the application is open, right-click on the title bar, select "*More
Actions*", and "*Special Application Settings*". This will open up a dialog for
*this application*".

.. figure:: {filename}images/x11-fullscreen/fullscreen-4.png
    :alt: Configuration Dialog
    :figwidth: 300px
    :align: left
    :target: |filename|/images/x11-fullscreen/fullscreen-4.png

    The "Special Application Settings" dialog.

The "*Size & Position*" tab contains the option we are looking for: "*Obey geometry restrictions*".

Override the WM default by ticking the checkbox and selecting "*Force*" in the drop-down menu and setting the value to "*No*".

.. figure:: {filename}images/x11-fullscreen/fullscreen-5.png
    :alt: The geometry restriction option.
    :figwidth: 300px
    :align: left
    :target: |filename|/images/x11-fullscreen/fullscreen-5.png

    Close-up on the value that you need to set.


.. raw:: html

    <br clear="both" />


End-Result
----------

.. figure:: {filename}images/x11-fullscreen/fullscreen-6.png
    :alt: Screenshot after changing the option.
    :figwidth: 300px
    :align: left
    :target: |filename|/images/x11-fullscreen/fullscreen-6.png

    In this screenshot, you can see that the gap between both windows has
    disappeared.

After changing these values you can try to maximise the window (or restore,
then maximise again). It should now fill the screen up to the last pixel,
closuing up the gap.

This fix is applicable to all applications which force size increments on your
window. For me, this was both *gvim* and *xterm*, but it will surely also fix
issues with *emacs*.

This fix is also not exclusive to KDE. For example "*awesome*" allows you to do
the same `via config files`_, and I am sure other WMs let you override this as
well.


.. _via config files: http://superuser.com/questions/751075/emacs-maximized-but-leaves-few-pixels-in-awesome-wm
