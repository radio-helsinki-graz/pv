=================================
Radio Helsinki Program Management
=================================

Installation
============

To get setup you must have the following installed:

 * MySQL-Client Development libraries 
 * JPEG library development files
 * Python 2.7 including Development files
 * virtualenv 1.11

In Debian or Ubuntu (or derivatives) you should be able to achieve this with this command:

    $ sudo apt-get install libmysqlclient-dev libjpeg-dev python2.7-dev virtualenv


Setting up the environment
--------------------------

Create a virtual environment where the dependencies will live::

    $ virtualenv -p python2.7 python
    $ source python/bin/activate
    (python)$

Change into the base directory of this software and install the project dependencies::

    (python)$ pip install -r requirements.txt


Setting up the database
-----------------------

By default the project is set up to run on a SQLite database.  

Create a file pv/local_settings.py and add at least the line 

    SECRET_KEY = 'secret key'

(obviously replacing "secret key" with a key of you choice).

Then run::

    (python)$ python manage.py migrate
    (python)$ python manage.py loaddata program/fixtures/*.yaml


Adding an admin user
--------------------

In order to create an admin user (which you will need to login to the webinterface after the next step) run::

    (python)$ python manage.py createsuperuser


Running a web server
--------------------

In development you should run::

    (python)$ python manage.py runserver

After this you can open http://127.0.0.1:8000/admin in your browser and log in with the admin credential you created previously.

