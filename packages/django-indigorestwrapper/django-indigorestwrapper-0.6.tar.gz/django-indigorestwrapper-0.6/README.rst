Introduction
============

IndigoRESTWrapper is intended to provide more complete access to the information in the Indigo database.

This is a (completely unauthorized) wrapper for Indigo (http://www.indigodomo.com/), using 
Django (https://www.djangoproject.com/) and Django-rest-framework (http://www.django-rest-framework.org/).

It can do two things:
 - wrap (some of) the current REST calls, in case you'd like different authentication (the authentication provided by django 
   REST is detailed here: http://www.django-rest-framework.org/api-guide/authentication/)
 - provide a few new acccessors, such as retrieving a device by its 'id' and also providing a view of the history of a device.

Technically it works by either just calling the current Indigo REST api, or for information which isn't available there, scanning the database file(s).

Currently available APIs:
  - http://localhost:8000/devices/ 
    - returns a list of all the details about all the devices. It's more detailed than Indigo's devices.json, but it's cached and so some values will certainly be out of date. However, you can use device_history to get this information.
  - http://localhost:8000/device/1838057829/
    - Complete information about the device with the matching device id. This is also cached and so some values will certainly be out of date. You can use device_history to get this information though.
  - http://localhost:8000/device_history/1838057829/
    - The history of the device. The exact format will depend on the type, but it will typically be a ts

There are also some which wrap the current Indigo API. The big problem here is simply that currently IndigoRESTWrapper can't interact with Indigo if Indigo is protected with authentication. This should be possible to fix relatively quickly, but one option is to block any access to indigo's port via your router's firewall, and then it doesn't matter so much that Indigo is unprotected.
  - http://localhost:8000/indigo_devices/
  - ... more to come

Installation
============
Before you start
----------------

If you don't know Django at all, you might want to follow the Django tutorial first:
https://docs.djangoproject.com/en/1.9/intro/

You should make sure you have an up-to-date version of pip:

.. code:: bash

  [sudo] pip install -U pip

Install virtualenv and virtualenvwrapper (if you haven't already):

.. code:: bash

  [sudo] pip install virtualenv
  [sudo] pip install virtualenvwrapper

BTW on default OSX pip installs to :
/Library/Frameworks/Python.framework/Versions/2.7/bin/virtualenvwrapper.sh

More details are here: http://virtualenvwrapper.readthedocs.org/ but a short version might be:

.. code:: bash

  cd $HOME
  mkdir .virtualenvs
  nano .bash_login

and to .bash_login you could add the following:

.. code:: bash

  export PROJECT_HOME=$HOME/Documents
  export PIP_PATH=/Library/Frameworks/Python.framework/Versions/2.7
  export WORKON_HOME=$HOME/.virtualenvs
  export VIRTUALENVWRAPPER_VIRTUALENV=$PIP_PATH/bin/virtualenv
  export VIRTUALENVWRAPPER_VIRTUALENV_ARGS='--no-site-packages'
  export PATH=$PATH:$PIP_PATH/bin
  source $PIP_PATH/bin/virtualenvwrapper.sh

The we need to set up the virtualenv:

.. code:: bash

  mkvirtualenv indigorestserver
  workon indigorestserver

Installing Django and django-indigorestwrapper
----------------------------------------------

First make a work directory:

.. code:: bash

  cd Documents
  mkdir IndigoRestWrapper
  cd IndigoRestWrapper

To install it you need to first install some dependencies:

.. code:: bash

  pip install django
  pip install djangorestframework

To check this package out now do:

.. code:: bash

  pip install django-indigorestwrapper

Create a new project:

.. code:: bash

  django-admin startproject mysite

Edit mysite/settings.py.

Add the following to INSTALLED_APPS:

.. code:: python

    'rest_framework',
    'indigorestwrapper',

DATABASES should look like:

.. code:: python

  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'indigo_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '/Library/Application Support/Perceptive Automation/Indigo 6/Logs/indigo_history.sqlite'),
    }
  }

(actually you're free to use whichever DB you prefer for default, but I'm keeping it sqlite3 for the benefit of this tutrorial)

At the end add:

.. code:: python

  REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
  }
  # INDIGO_URL = 'http://myserver.com:8176'
  INDIGO_URL = 'http://127.0.0.1:8176'

You might need to update the location for indigo_db in the DATABASES section (though what is above is the default) and INDIGO_URL at the end, to tell it where to find the indigo server.

Then, in the project directory, do:

.. code:: bash

  ./manage.py migrate 
  ./manage.py makemigrations

And finally, to try to grab the device data from indigo, do:

.. code:: bash

  ./manage.py updateindigodb

(Currently this requires indigo to be unprotected - you could always disable it to run this command, then re-enable it when done - though of course any forwarding of indigo commands will not work once the server is password protected again)

Now you should be able to get a server up and running using:

.. code:: bash

  ./manage.py runserver

(This is just for debugging - you should really set something up with e.g. Apache)
