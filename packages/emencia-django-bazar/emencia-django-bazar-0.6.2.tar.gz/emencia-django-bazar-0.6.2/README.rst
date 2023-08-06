.. _Django: https://www.djangoproject.com/
.. _South: http://south.readthedocs.org/en/latest/
.. _rstview: https://github.com/sveetch/rstview
.. _autobreadcrumbs: https://github.com/sveetch/autobreadcrumbs
.. _django-braces: https://github.com/brack3t/django-braces/
.. _django-crispy-forms: https://github.com/maraujop/django-crispy-forms
.. _Django-CodeMirror: https://github.com/sveetch/djangocodemirror
.. _RestructuredText: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html
.. _jQuery-Tags-Input: https://github.com/xoxco/jQuery-Tags-Input
.. _crispy-forms-foundation: https://github.com/sveetch/crispy-forms-foundation
.. _django-taggit: https://github.com/alex/django-taggit
.. _django-taggit-templatetags2: https://github.com/fizista/django-taggit-templatetags2/
.. _django-localflavor: https://github.com/django/django-localflavor
.. _django-sendfile: https://github.com/johnsensible/django-sendfile

Emencia Django Bazar
====================

A Django app to store basic informations about related entities (like customers, suppliers, ourselves, etc..).

.. Warning::
    Since 0.6.0 version, Django <= 1.8 support has been dropped, South migrations have moved to ``south_migration``, initial Django migration start from last south migration and so if you want to upgrade you will need to fake the initial migration.

Requirements
************

* Django >= 1.8;
* `autobreadcrumbs`_;
* `django-braces`_;
* `rstview`_;
* `Django-CodeMirror`_;
* `crispy-forms-foundation`_;
* `django-taggit`_;
* `django-taggit-templatetags2`_;
* `django-localflavor`_;
* `django-sendfile`_;


Features
********

* Note cards for entities: can contains content text or/and a file attachment;
* Optional markup into note cards content (default is no markup, `RestructuredText`_ is easily available);
* `Django-CodeMirror`_ usage if markup is used with RestructuredText;
* Assets management with django-assets;
* **i18n** usage for front interface;
* Templates prototyped with Foundation5;
* Tags for note cards using `jQuery-Tags-Input`_ into form;

Links
*****

* Download his `PyPi package <https://pypi.python.org/pypi/emencia-django-bazar>`_;
* Clone it on his `Github repository <https://github.com/sveetch/emencia-django-bazar>`_;

Install
*******

Add bazar app and its requirements to your installed apps in settings : ::

    INSTALLED_APPS = (
        ...
        'autobreadcrumbs',
        'localflavor',
        'taggit',
        'taggit_templatetags2',
        'djangocodemirror',
        'sendfile',
        'bazar',
        ...
    )

Then add its settings : ::

    from bazar.settings import *

See the app ``settings.py`` file to see what settings you can override.

Also there is some settings for requirements: taggit, djangocodemirror and sendfile. See their documentation for more details how to configure them properly.

And add its views to your main ``urls.py`` : ::

    from django.conf.urls import url, patterns
    from filebrowser.sites import site as filebrowser_site

    urlpatterns = patterns('',
        ...
        url(r'^bazar/', include('bazar.urls', namespace='bazar')),
        ...
    )

Finally install app models in your database using Django migrations: ::

    python manage.py migrate
