=============================
django-fever-notifications
=============================

.. image:: https://badge.fury.io/py/django-fever-notifications.png
    :target: https://badge.fury.io/py/django-fever-notifications

.. image:: https://travis-ci.org/Feverup/django-fever-notifications.png?branch=master
    :target: https://travis-ci.org/Feverup/django-fever-notifications

Generic models for implement message based features

Documentation
-------------

The full documentation is at https://django-fever-notifications.readthedocs.org.

Quickstart
----------

Install django-fever-notifications::

    pip install django-fever-notifications

Then use it in a project:


.. code-block :: python

    from fevernotifications.models import Notification
    from fevernotifications.shortcuts import create_notification

    # Create a notification
    create_notification(user, title="Hello", message="Hello world!")

    # Query all notifications per user
    Notification.objects.by_target(user)


Features
--------

* TODO

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements-test.txt
    (myenv) $ python runtests.py

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-pypackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
