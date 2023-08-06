=====================
Django Hosted Plugins
=====================

Django Hosted Plugins is used to host third-party plugins that work alongside
your project but cannot be hosted on first-party plugin repositories
due to restrictions imposed.

This project was started to overcome restrictions imposed by WordPress.com
and is currently favoured towards hosting WordPress plugins.

Requires Django and Django REST Framework. It is untested and comes AS-IS.

Quick start
-----------

1. Add "rest_framework" and "hosted_plugins" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'rest_framework',
        'hosted_plugins',
    ]

2. Include the plugins URLconf in your project urls.py like this::

    url(r'^plugins/', include('hosted_plugins.urls')),

3. [OPTIONAL] Include login URLs for the browsable API. (See here for details: http://www.django-rest-framework.org/tutorial/quickstart/#urls)::

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

4. Install pytz if you're using a database that will require it for querying datetime fields::

    pip install pytz

5. Run `python manage.py migrate` to create the hosted_plugins models.

6. Use the Django admin to add plugins, or use a script to automate it.
