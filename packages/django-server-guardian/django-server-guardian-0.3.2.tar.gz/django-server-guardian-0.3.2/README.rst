Django Server Guardian
======================

A reusable Django app, that fetches and visualizes server health metrics.

The data is fetched from the `API app`_, that is installed on the client server.

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-server-guardian

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/bitmazk/django-server-guardian.git#egg=server_guardian

TODO: Describe further installation steps (edit / remove the examples below):

Add ``server_guardian`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'server_guardian',
    )

Add the ``server_guardian`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^server-guardian/', include('server_guardian.urls')),
    )


Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate server_guardian


For simple color highlighting of the server status, you can include the following
line to your template:

.. code-block:: html

        <link href="{% static "server_guardian/css/styles.css" %}" rel="stylesheet">


Reload now button
^^^^^^^^^^^^^^^^^

The ``server_list.html`` template includes a reload now button, which is useful
for testing or if you don't want to wait for the cron job to fire again.
It requires ``jQuery`` and if you want to keep the default template, make sure,
you have an ``extrajs`` block in your ``main.html`` template.

Note, that atm this will reload all servers, so it might take a bit
if you have many servers configured.

Usage
-----

Once you've installed the `API app`_ on the client server and added some
endpoitns to your settings, as described there, you can go ahead and configure
your servers.

Visit the Django admin for the server guardian, create a new ``Server`` object
and fill out the fields.

:API URL: This is the url, the `API app`_ is hooked in under on the client server.
:Server name: You can simply name the server.
:Token: You will need to create a token string, that you'll add here and on the remote server.

The other fields are not to be edited and they will be overwritten every time the
guardian fetches new data.

Finally you should schedule the management command ``guardian_fetch`` to run
as often as you wish to update your server status (e.g. with cron).

Visit ``/server-guardian/`` for health status overview.

Settings
--------

There are a few settings, you can work with.

DJANGO_PROJECT_ROOT (mandatory!)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It's likely, that you already have this setting. If not, please set it to
the directory where your ``manage.py`` file is located.

SERVER_GUARDIAN_EMAIL_ON_STATUS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sets on which HTML status codes to send an email to the admins.

Default: ``SERVER_GUARDIAN_EMAIL_ON_STATUS = [403, 404, 405]``

SERVER_GUARDIAN_DASHBOARD_VIEW_PERMISSION
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This setting gets a function assigned, that is passed to the
``user_passes_test`` decorator in the dashboard view.

Default: ``SERVER_GUARDIAN_DASHBOARD_VIEW_PERMISSION = lambda u: u.is_superuser``

Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    mkvirtualenv -p python2.7 django-server-guardian
    make develop

    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch

In order to run the tests, simply execute ``tox``. This will install two new
environments (for Django 1.6 and Django 1.7) and run the tests against both
environments.

.. _API app: https://github.com/bitmazk/django-server-guardian-api
