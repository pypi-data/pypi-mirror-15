Test application for :mod:`django_turnit`
=========================================

This application will demonstrate how to use django_turnit with a generic test application.

Installation
------------

Copy the example project into a fresh folder, add a virtualenv.

Folder structure :
^^^^^^^^^^^^^^^^^^

.. code:: sh

    $ tree -I 'virtualenv*'
    .
    ├── media_test
    │   ├── apprendre_python3.pdf
    │   ├── HTML_and_CSS.pdf
    │   ├── linux_bash_cheatsheet.pdf
    │   ├── python_notes.pdf
    │   └── test_single_page.pdf
    ├── project
    │   ├── appz
    │   │   ├── admin.py
    │   │   ├── admin.pyc
    │   │   ├── __init__.py
    │   │   ├── __init__.pyc
    │   │   ├── migrations
    │   │   │   ├── 0001_initial.py
    │   │   │   ├── 0001_initial.pyc
    │   │   │   ├── __init__.py
    │   │   │   └── __init__.pyc
    │   │   ├── models.py
    │   │   ├── models.pyc
    │   │   ├── tests.py
    │   │   └── views.py
    │   ├── db.sqlite3
    │   ├── manage.py
    │   └── project
    │       ├── __init__.py
    │       ├── __init__.pyc
    │       ├── settings.py
    │       ├── settings.pyc
    │       ├── urls.py
    │       └── wsgi.py
    ├── README.rst
    └── requirements.txt


On linux
^^^^^^^^

Initial installation

.. code:: sh

    $ cd <project_root>/..
    $ mkdir virtualenv
    $ virtualenv ./virtualenv
    $ source ./virtualenv/bin/activate
    $ pip install pip --upgrade
    $ pip install --requirement ./requirement.txt
    $ cd project
    $ ./manage.py test  # Checks the setup
    $ ./manage.py createsuperuser
    $ ./manage.py migrate
    $ ./manage.py runserver



Data initialization
-------------------

The application comes with a few PDF documents to test. Those PDF files are stored in the media_test folder.


