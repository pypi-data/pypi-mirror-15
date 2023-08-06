Eckerd Django Google SSO
============

A reusable django application for google sso

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install eckerd-django-google-sso

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/christopherdavenport/eckerd-django-google-sso.git#egg=eckerd-django-google-sso

TODO: Describe further installation steps (edit / remove the examples below):

Add ``eckerd-django-google-sso`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'eckerd-django-google-sso',
        'social.apps.django_app.default',
        'django12factor',
    )

Add the ``eckerd-django-google-sso`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = [
        url(r'^/', include('eckerd-django-google-sso.urls')),
    ]

Before your tags/filters are available in your templates, load them by using

.. code-block:: html

	{% load backend_utils %}


Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate


Usage
-----

Simple Wrap Your Content In a @LOGIN_REQUIRED

Finally Drop These Settings In Place In The Final Application

.. code-block:: python

    AUTHENTICATION_BACKENDS = (
        'social.backends.google.GoogleOAuth2',
        'django.contrib.auth.backends.ModelBackend',
    )

    AUTH_USER_MODEL = 'eckerd-django-google-sso.CustomUser'
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    LOGIN_URL = '/login/'
    LOGIN_REDIRECT_URL = '/'
    URL_PATH = ''
    SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
    SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'

    # Google OAuth2 (google-oauth2)
    SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
    SOCIAL_AUTH_GOOGLE_OAUTH2_USE_UNIQUE_USER_ID = True
    SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ['eckerd.edu']
    SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ]

    SOCIAL_AUTH_PIPELINE = (
        'social.pipeline.social_auth.social_details',
        'social.pipeline.social_auth.social_uid',
        'social.pipeline.social_auth.auth_allowed',
        'social.pipeline.social_auth.associate_by_email',
        'social.pipeline.social_auth.social_user',
        'social.pipeline.user.get_username',
        'social.pipeline.user.create_user',
        'social.pipeline.social_auth.associate_user',
        'social.pipeline.social_auth.load_extra_data',
        'social.pipeline.user.user_details'
    )


    SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['first_name', 'last_name', 'email',
                                            'username']


    custom_settings = (
        'SOCIAL_AUTH_GOOGLE_OAUTH2_KEY',
        'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET',
    )

    import django12factor

    d12f = django12factor.factorise(custom_settings=custom_settings)
    DATABASES = d12f['DATABASES']
    SECRET_KEY = d12f['SECRET_KEY']
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = d12f['SOCIAL_AUTH_GOOGLE_OAUTH2_KEY']
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = d12f['SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET']
    ALLOWED_HOSTS = d12f['ALLOWED_HOSTS']
    DEBUG = d12f['DEBUG']
    LOGGING = d12f['LOGGING']


Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    mkvirtualenv -p python2.7 eckerd-django-google-sso
    make develop

    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch

In order to run the tests, simply execute ``tox``. This will install two new
environments (for Django 1.8 and Django 1.9) and run the tests against both
environments.
