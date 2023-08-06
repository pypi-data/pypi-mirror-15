==========
Reviewable
==========
Reviewable provides simple, customizable reviews for any of your Django models. The templates for each of your reviewable
models can be customised with ease.

Quick Start
-----------
1.

.. code-block:: bash

    $ pip install django-reviewable

2. Add "Reviewable" to your INSTALLED_APPS setting:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'Reviewable',
        ...
    ]

2. Include the Reviewable URLconf in your projects urls.py:

.. code-block:: python

    url(r'^reviews/', include('Reviewable.urls', namespace='Reviewable')),

2. Run ``python manage.py migrate``

5. Add the mixin ``Reviewable`` to any model you want to be reviewable.

.. code-block:: python

        ...
        from Reviewable.models import Reviewable
        ...

        class ReviewableModel(models.Model, Reviewable):
            ...

Custom Templates
----------------
Reviewable allows you to customise the templates for each reviewable model. Furthemore, the reviewable object is magically
made available in the template context.

For example:
    1. You have a model called ``Hotel`` in an app called ``Hotel``
    2. You want a custom template for the review creation view
    3. You would add a template in ``Hotel/templates/Hotel`` called ``hotel_review_create.html``
        - Note: This the template name has to be in camel case and all lower case
    4. The hotel object is made available in the template context by the usual ``{{ hotel }}`` tag
    5. This can be repeated for templates for all views: ``hotel_review_list.html``, ``hotel_review_update.html``,
       ``hotel_review_confirm_delete.html`` and ``hotel_review_detail.html``

Template Tags
-------------

Reviewable provides one simple but useful template inclusion tag that will include controls for your reviewable object.

To use this just load in the template tag:

.. code-block:: python

    {% load reviewable %}
    ...
    {% show_review_controls reviewable_object %}

The template for the inclusion tag is very basic so it is a good idea to override it in the usual Django fashion.
The name of the template is "Reviewable/__review_controls.html".

Post Delete Signals
-------------------

Deletion of a reviewable object won't automatically cause a cascade delete of all of the objects reviews. Hence, it
is a good idea to use the post delete signal somewhere in your app as below:

.. code-block:: python

    from MyApp.models import ReviewableModel
    from django.db.models.signals import post_delete
    ...

    post_delete.connect(ReviewableModel.delete_reviews, sender=ReviewableModel)

Settings
--------

All settings are shown below with their defaults.

REVIEW_RATING_CHOICES
+++++++++++++++++++++

.. code-block:: python

    REVIEW_RATING_CHOICES=(
        (1, '1 Star'),
        (2, '2 Star'),
        (3, '3 Star'),
        (4, '4 Star'),
        (5, '5 Star')
    )

REVIEW_DELETE_SUCCESS_URL
+++++++++++++++++++++++++

.. code-block:: python

    REVIEW_DELETE_SUCCESS_URL='/'

REVIEW_STREAM_ENABLED
+++++++++++++++++++++

Reviewable can utilise GetStream if required. This would mean reviews are automatically published to your GetStream.io
feed. See https://github.com/GetStream/stream-django for more information

.. code-block:: python

    REVIEW_STREAM_ENABLED=False
