.. image:: https://img.shields.io/codeship/8c6d7510-148d-0134-3d1b-7a5ab8a25fce/default.svg
   :target: https://bitbucket.org/hellwig/django-integrator
.. image:: https://coveralls.io/repos/bitbucket/hellwig/django-integrator/badge.svg?branch=default 
   :target: https://coveralls.io/bitbucket/hellwig/django-integrator?branch=default
.. image:: https://img.shields.io/pypi/v/django-integrator.svg
   :target: https://pypi.python.org/pypi/Django-Integrator/
   

#################
Django Integrator
#################

What is it?
===========
- A library to conveniently import and use an integrator compliant applications.
- A tool for stating a new Django project with the focus on creating a single
  distributable application.


What problem does it solve?
===========================
An integrator compliant distributable application contains its own settings and
url file, which using the library can than be imported into the main settings
file. This way the main settings file can be kept relatively clean and simple
thus being more the 'server' part of the Django install.
This made it easier for me to split my django project out in several different
applications, which improved modularity, maintainability and readability.


How do I install it?
====================
pip install django-integrator


How do I use it?
================
As stated above there are two use cases, create and library.

Create
------
To create a new project go to the folder where you want the new project to be
created in. Then issue the command: 
$ django-integrator-create pypi_name django_app_class_name verbose_name author email
The parameters mean the following:

pypi_name:
  The name of this application as it would be in the PyPI register, the program
  will do a query to determine if the name is available (at the time).
  The actual importable name will be the pypi_name with '-' replaced with
  underscores.
 
django_app_class_name:
  The name that the application class (as in the apps.py) will have in Django.

verbose_name:
  The name as the app will be displayed in, for example, the admin interface.

author:
  Your name

email:
  Your email address

This will create a new project, with some additional files and adjusted layouts
compared to the default django one. Most notably, the interface folder contains
only just enough to get wsgi server set. The rest is stored in the app folder.
There is also a script calls devset.py which removes the current sqlite db,
deletes the lates migration file, recreates migration file, set the admin user
up with password admin and starts a development server.

The settings file in the app folder mirrors layout wise the same as the 'normal'
settings file with the exception that there is some extra logic for certain
configurations like middleware. Sometimes it is import that certain middleware
are imported before another one. To achieve this just put your middleware in
followed by the middleware it must precede. The library will detect that the
middleware already exist and will add your middleware before that one.

Furthermore it also creates a setup.py file, which can be used as a base to
upload the app to PyPi.


Library
-------
At the end of the inteface.settings file you see the following lines:
>>> import django_integrator
>>> django_integrator.add_application('your_app_name')
To add more applications to your system simply repeat the last line.

URL wise you can see that in interface.urls the following lines are at the end
>>> import django_integrator
>>> django_integrator.add_urlpatterns(urlpatterns)

This will add all the applications urls to the server urls file, be careful as
this will overwrite previous defined urls if the path clashes.


What license is this?
=====================
Two-clause BSD, this license is also used when creating a new application with
this tool, obviously this is just a template and you can change the license in
your own application to whatever you think is the most appropriate. However I
would like to encourage you not to change the license and perhaps even consider
uploading your app to pypi.

How can I get support?
======================
The tools I publish have already taken me considerable effort which I have given
away free of charge, if you require guaranteed support please contact me via
e-mail so we can discuss my fee.

How can I give you support?
===========================
Feedback, suggestions and comments via the repo's bug tracker are always
appreciated. Time permitting I will have a serious look at any pull requests. 

Can I do something more that this?
----------------------------------
Wow! Are you sure? Well if you are really sure, and that would be fantastic, you
can leave your donation in the tip hat AKA patreon account;
http://patreon.com/hellwig 

Thank you very much! Your donation will help me towards my end-goal of a
grid-independent small holding where I automate the sh*t out of it :-). In the
mean time I'll keep building stuff and where possible and practical open-source
them under the BSD license.  





