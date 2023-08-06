.. image:: https://travis-ci.org/knowledge4life/django-onmydesk.svg?branch=develop
    :target: https://travis-ci.org/knowledge4life/django-onmydesk


Django - OnMyDesk
===================

A Django app to build reports in a simple way.

Installation
------------

With pip::

  pip install django-onmydesk

Add 'onmydesk' to your INSTALLED_APPS::

  INSTALLED_APPS = [
      # ...
      'onmydesk',
  ]

Run `./manage.py migrate` to create **OnMyDesk** models.

Quickstart
-----------

To create reports we need to follow just two steps:

    1. Create a report class in our django app.
    2. Add this report class to a config in you project settings to enable **OnMyDesk** to see your reports.

So, let's do it!

Create a module called *reports.py* in you django app with the following content:

myapp/reports.py::

    from onmydesk.core import reports

    class UsersReport(reports.SQLReport):
        name = 'Users report'
	query = 'SELECT * FROM auth_user'

On your project settings, add the following config::

    ONMYDESK_REPORT_LIST = [
	'myapp.reports.UsersReport',
    ]

Each new report must be added to this list. Otherwise, it won't be shown on admin screen.

Now, access your **OnMyDesk** admin screen and you'll see your **Users report** available on report creation screen.

After you create a report, it'll be status settled up as 'Pending', to process it you must run `process` command. E.g::

  $ ./manage.py process
  Found 1 reports to process
  Processing report #29 - 1 of 1
  Report #29 processed
