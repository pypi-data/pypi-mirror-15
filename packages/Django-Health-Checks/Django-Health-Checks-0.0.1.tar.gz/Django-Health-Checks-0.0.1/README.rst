Django-Health-Checks
================

`Django-Health-Checks`_ is Django plugin which adds a few
health check endpoints (ping, time, and status) to the Django project.

Add *health_checks* to your settings.py *INSTALLED_APPS*

::

    INSTALLED_APPS += ('health_checks',)

Add *health_checks* urls

::

    import health_checks

    urlpatterns += [
        url('r^', include('health_checks.urls')),
    ]

::

    from health_checks import status_job

    @status_job(name="PostgreSQL", timeout=5)
    def postgresql():
        # Perform a ping/query to Postgres

    @status_job
    def facebook
        # Ping some Facebook service.


get Django-Health-Checks
====================

Install `django`_

    sudo easy_install Django-Health-Checks
    or
    sudo pip install Django-Health-Checks

Download the latest release from `Python Package Index`_
or clone `the repository`_

.. _Python Package Index: https://pypi.python.org/pypi/Django-Health-Checks
.. _Django-Health-Checks: http://packages.python.org/Django-Health-Checks
.. _Django: http://flask.pocoo.org/
.. _the repository: https://github.com/juztin/django-health-checks
