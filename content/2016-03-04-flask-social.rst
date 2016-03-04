Getting Flask-Social working
############################


:date: 2016-03-04 21:17:42
:tags: flask, python
:category: programming


A couple of weeks ago I decided to add social login buttons to a small
web-page. I am usually wary of "frameworks" and "plugins", and usually only use
them sparingly. I *do* use Flask for web-development though.

For a change I decided to give flask-social_ a chance. Turns out that one is
based on flask-security_ so I had to ditch flask-login_ and that's where the
fun started.


Flask Security
--------------

First, flask-security *enforces* that ``user`` and ``group`` DB table have an
``id`` column. Historically, the PK in my DB is the email address though. Even
"simulating" an ``id`` column using a ``property`` did not work. Took me a
while to figure out the problem as all errors are silent.

Eventually gave up and added an auto-incrementing ``id`` for both tables
anyway. That made it work. So yay...


Flask Social
------------

This was the worst minefield. For the most part because the documentation is
wrong. Starting off from their "getting started" section of version 1.6.2 won't
get you working social logins. There are several issues:

* Not all mentioned modules are Python 3 compatible (flask-social being one of
  them).
* The installation of the social "providers" is not completely doable via pip.
  Not all packages are available on pypi.
* The profile route breaks as some connections may become ``None``. This is
  easily fixed by some conditionals.
* Removing a social connection does not work as the associated route does not
  allow the ``DELETE`` method. The only workaraound I found was an XhrIO call.

All in all, the solution is simple. But getting there was not trivial. For two
reasons: One, beaker signals make it hard to follow the flow of the
applications, and two, flask-social uses ``*args`` and ``**kwargs`` exessively.
The latter makes it really hard to reason which parameters get passed on to
which function.


My (current) solution
---------------------

.. note::
    This document should be read as a companion to the current Flask-Social
    docs in case you want to get it to work on Python 3. The official docs are
    here:

    http://pythonhosted.org/Flask-Social/#getting-started

After much fiddling around, I came up with the following solution. It still
requires a lot of cleanup, but at least, this is a working solution.

Assuming you have flask-security properly configured, these are the steps to
follow:

* For Python 3, install flask-social from my github branch (You may want to
  check first if the pypi version has since been updated)::

    pip install https://github.com/exhuma/flask-social/tarball/python3-support

* Again for Facebook login with Python 3, install the Facebook API from github
  (and check pypi first of course)::

    pip install http://github.com/pythonforfacebook/facebook-sdk/tarball/master

* ... the same goes for python-twitter::

    pip install git+https://github.com/bear/python-twitter

* The google provider seems to be fine.


This should get you set up for Python 3. On to the next step...


Application Setup
-----------------

Configuration
~~~~~~~~~~~~~

Something not well documented:

In case you need to pass on different OAuth scopes (f.ex.: getting e-mail
addresses from Google accounts), you need to set the ``'request_token_params``
key for your social provider:

.. code-block:: python

    app.config['SOCIAL_GOOGLE'] = {
        'consumer_key': '...',
        'consumer_secret': '...',
        'request_token_params': {
            'scope': ('https://www.googleapis.com/auth/userinfo.profile '
                      'https://www.googleapis.com/auth/plus.me '
                      'https://www.googleapis.com/auth/userinfo.email')

        }
    }


Data Model
~~~~~~~~~~

As mentioned earlier, flask-social uses ``**kwargs`` in places. This causes
problems with the ``rank`` argument. To fix this without modifying the
flask-social code, you can just override the ``__init__`` method of your
``Connection`` class to accept ``**kwargs`` as well. You then of course need to
set the values as needed. You also need to add a relationship to your ``User``
class:

.. code-block:: python

    class Connection(DB.Model):

        ...

        user = relationship('User')

        def __init__(self, *args, **kwargs):
            self.user_id = kwargs['user_id']
            self.provider_id = kwargs['provider_id']
            self.provider_user_id = kwargs['provider_user_id']
            self.access_token = kwargs['access_token']
            self.secret = kwargs['secret']
            self.display_name = kwargs['display_name']
            self.profile_url = kwargs['profile_url']
            self.image_url = kwargs['image_url']
            self.rank = kwargs.get('rank')


Passing connections to your template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is tivial. Some connections may be ``None``. As such, you need to check
those before calling ``get_connection`` on them. Additionally, you need to
allow the ``DELETE`` method so you can remove connections. This *seems* to be
caused by a redirect which is used internally in flask-social. This redirect
happens *after* the connection has been deleted. So you will land on this
endpoint, still using the ``DELETE`` method. I simply accept it here, and don't
treat it in a special manner. This is not fully HTTP compliant, but at least it
works:

.. code-block:: python

    @app.route('/profile', methods=['GET', 'DELETE'])
    @login_required
    def profile():
        return render_template(
            'profile.html',
            content='Profile Page',
            twitter_conn=social.twitter.get_connection() if social.twitter else None,
            facebook_conn=social.facebook.get_connection() if social.facebook else None,
            google_conn=social.google.get_connection() if social.google else None)


Talking about disconnecting. The flask-social docs use a ``FORM`` element with
``action="DELETE"``. This did not work for me and had to replace it with an
XhrIO call (even though this uses closure, the gist should be understandable):

.. code-block:: javascript

    var disconnectButtons = goog.dom.getElementsByClass('social-disconnect-button');
    goog.array.forEach(disconnectButtons, function(element) {
      goog.events.listen(element, goog.events.EventType.CLICK, function(evt) {
        var span = goog.dom.getAncestorByTagNameAndClass(evt.target, 'span');
        var providerId = span.getAttribute('data-provider-id');
        var userId = span.getAttribute('data-user-id');
        var connectionURL = '/connect/' + providerId + '/' + userId;
        goog.net.XhrIo.send(connectionURL, function(evt) {
          var xhr = evt.target;
          if (xhr.isSuccess()) {
            window.location.reload(true);
          } else {
            var alertDialog = new goog.ui.Dialog();
            alertDialog.setContent('Verbindungstrennung fehlgeschlagen.');
            alertDialog.setTitle('Fehler');
            alertDialog.setButtonSet(goog.ui.Dialog.ButtonSet.OK);
            alertDialog.setVisible(true);
          }
        }, 'DELETE');
      });
    });

In order to get a consistend look & feel, I used the same way for the login
button and to create connections. This may seem hacky, but it's consisten in
both source-code and UI. I had to use form submits in this case to get around
the same-origin policy:

.. code-block:: javascript

    var loginButtons = goog.dom.getElementsByClass('login-button');
    goog.array.forEach(loginButtons, function(element) {
      goog.events.listen(element, goog.events.EventType.CLICK, function(evt) {
        var form = goog.dom.getAncestorByTagNameAndClass(evt.target, 'form');
        form.submit();
      });
    });

    var connectButtons = goog.dom.getElementsByClass('social-connect-button');
    goog.array.forEach(connectButtons, function(element) {
      goog.events.listen(element, goog.events.EventType.CLICK, function(evt) {
        var form = goog.dom.getAncestorByTagNameAndClass(evt.target, 'form');
        form.submit();
      });
    });



.. _flask-social: https://pythonhosted.org/Flask-Social
.. _flask-security: https://pythonhosted.org/Flask-Security/
.. _flask-login: https://flask-login.readthedocs.org/en/latest/
