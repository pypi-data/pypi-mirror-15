=============
Registrations
=============

Registrations is a Django app that allows users to register using
email or mobile phone (SMS), then sends out a verification code
via that method for the user to use when confirming their account
to activate their account.

Quick start
-----------

1. Add "registrations" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'registrations',
    )

2. Run `python manage.py migrate` to create the registrations models.
