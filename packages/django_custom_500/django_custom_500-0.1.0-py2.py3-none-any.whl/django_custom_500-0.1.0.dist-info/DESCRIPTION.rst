Django custom 500
=================

|Travis CI Badge| Â  |Coverage Status| Â  |Requirements Status|

Installation
------------

.. code:: bash

    pip install --upgrade django-custom-500

**Add ``django_custom_500`` to ``INSTALLED_APPS``:**

.. code:: python

    INSTALLED_APPS = (
        'django_custom_500',
    )

Usage
-----

Create ``500.html`` in your ``template`` folder.

**OR**

Set ``CUSTOM_500_TEMPLATE`` in your settings.

Example:

.. code:: python

    CUSTOM_500_TEMPLATE = "my/path/to/500.html"

.. |Travis CI Badge| image:: https://api.travis-ci.org/illagrenan/django-custom-500.png
   :target: https://travis-ci.org/illagrenan/django-custom-500
.. |Coverage Status| image:: https://coveralls.io/repos/illagrenan/django-custom-500/badge.svg?branch=master
   :target: https://coveralls.io/r/illagrenan/django-custom-500?branch=master
.. |Requirements Status| image:: https://requires.io/github/illagrenan/django-custom-500/requirements.svg?branch=master
   :target: https://requires.io/github/illagrenan/django-custom-500/requirements/?branch=master


