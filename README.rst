=================================
Radio Helsinki Program Management
=================================

Installation
============

To get setup you must have the following installed:

 * Python 2.7
 * virtualenv 1.11

Setting up the environment
--------------------------

Create a virtual environment where the dependencies will live::

    $ virtualenv --no-site-packages helsinki
    $ source helsinki/bin/activate
    (helsinki)$

Install the project dependencies::

    (helsinki)$ pip install -r requirements.txt

Setting up the database
-----------------------

By default the project is set up to run on a SQLite database.  You can run::

    (helsinki)$ python manage.py syncdb
    (helsinki)$ python manage.py loaddata program/fixtures/*.yaml

Running a web server
--------------------

In development you should run::

    (helsinki)$ python manage.py runserver
