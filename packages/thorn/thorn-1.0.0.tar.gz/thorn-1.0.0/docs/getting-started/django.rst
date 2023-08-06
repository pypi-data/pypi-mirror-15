.. _django-guide:

=============================================================================
                             Django Integration
=============================================================================

.. contents:: Table of Contents:
    :local:
    :depth: 1

.. _django-installation:

Installation
============

To use Thorn with your Django project you must

#. Install Thorn

   .. code-block:: console

        $ pip install thorn

#. Add ``thorn.django`` to ``INSTALLED_APPS``:

   .. code-block:: python

        INSTALLED_APPS = (
            # ...,
            'thorn.django',
        )

#. Migrate your database to add the subscriber model:

    .. code-block:: console

        $ python manage.py migrate

#. Webhook-ify your models by adding the ``webhook_model`` decorator.

    Read all about it in the :ref:`Events Guide <events-guide>`.

#. (Optional) Install views for managing subscriptions:

    Only :ref:`Django REST Framework <django-rest-framework>` is supported
    yet, please help us by contributing more view types.

.. _django-rest-framework:

Django Rest Framework Views
===========================

The library comes with a standard set of views you can add to your
Django Rest Framework API, that enables your users to subscribe and
unsubscribe from events.

The views all map to the :class:`~thorn.django.models.Subscriber` model.

To enable them add the following URL configuration to your
:file:`urls.py`:

.. code-block:: python

    url(r"^hooks/",
        include("thorn.django.rest_framework.urls", namespace="webhook"))

.. _django-rest-framework-operations:

Supported operations
--------------------

.. note::

    All of these curl examples omit the important detail
    that you need to be logged in as a user of your API.

.. django-rest-framework-subscribe:

Subscribing to events
~~~~~~~~~~~~~~~~~~~~~

Adding a new subscription is as simple as posting to the ``/hooks/`` endpoint,
including the mandatory event and url arguments:

.. code-block:: bash

    $ curl -X POST                                                      \
    > -H "Content-Type: application/json"                               \
    > -d '{"event": "article.*", "url": "https://e.com/h/article?u=1"}' \
    > http://example.com/hooks/

Returns the response:

.. code-block:: json

    {"uuid": "c91fe938-55fb-4190-a5ed-bd92f5ea8339",
     "url": "http:\/\/e.com\/h/article?u=1",
     "created_at": "2016-01-13T23:12:52.205785Z",
     "updated_at": "2016-01-13T23:12:52.205813Z",
     "user": 1,
     "content_type": "application\/json",
     "subscription": "http://localhost/hooks/c91fe938-55fb-4190-a5ed-bd92f5ea8339",
     "event": "article.*"}

**Parameters**

- ``event`` (mandatory)

    The type of event you want to receive notifications about.  Events are
    composed of dot-separated words, so this argument can also be specified
    as a pattern matching words in the event name (e.g. ``article.*``,
    ``*.created``, or ``article.created``).

- ``url`` (mandatory)

    The URL destination where the event will be sent to, using
    a HTTP POST request.

- ``content_type`` (optional)

    The content type argument specifies the MIME-type of the format
    required by your endpoint.  The default is ``application/json``,
    but you can also specify ``application/x-www-form-urlencoded.``.

The only important part of the response data at this stage is the ``uuid``,
which is the unique identifier for this subscription, and the ``subscription`` url
which you can use to unsubscribe later.

.. _django-rest-framework-list-subscriptions:

Listing subscriptions
~~~~~~~~~~~~~~~~~~~~~

Perform a *GET* request on the ``/hooks/`` endpoint to retrieve a list of
all the subscriptions owned by user:

.. code-block:: bash

    $ curl -X GET                                       \
    > -H "Content-Type: application/json"               \
    > http://example.com/hooks/

Returns the response:

.. code-block:: json

    {"previous": null,
     "results": [
        {"uuid": "c91fe938-55fb-4190-a5ed-bd92f5ea8339",
         "url": "http:\/\/e.com\/h/article?u=1",
         "created_at": "2016-01-15T23:12:52.205785Z",
         "updated_at": "2016-01-15T23:12:52.205813Z",
         "user": 1,
         "content_type": "application\/json",
         "event": "article.*"}
     ],
     "next": null}

.. _django-rest-framework-unsubscribe:

Unsubscribing from events
~~~~~~~~~~~~~~~~~~~~~~~~~~

Perform a *DELETE* request on the ``/hooks/<UUID>`` endpoint to unsubscribe
from a subscription by unique identifier:

.. code-block:: bash

    $ curl -X DELETE                                    \
    > -H "Content-Type: application/json"               \
    > http://example.com/hooks/c91fe938-55fb-4190-a5ed-bd92f5ea8339

Example endpoint
================

This is an example Django webhook receiver view, using the json content type:

.. code-block:: python

    from __future__ import absolute_import, unicode_literals

    import json

    from django.http import HttpResponse
    from django.views.decorators.http import require_POST
    from django.views.decorators.csrf import csrf_exempt

    @require_POST()
    @csrf_exempt()
    def handle_article_changed(request):
        payload = json.loads(request.body)
        print('Article changed: {0[ref]}'.format(payload)
        return HttpResponse(status=200)


Using the :func:`~django.views.decorators.csrf.csrf_exempt` is important here,
as by default Django will refuse POST requests that do not specify the CSRF
protection token.
