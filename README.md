install locally this package

`pip install virtualenv`

and you should be able to double check the installation with

`virtualenv --version`

## Create Virtual Environment

A virtual environments allows to have a folder with all the dependencies only in that folder.

Hence create your local folder `mkdir hello_world_django; cd hello_world_django`

Then create the virtual environment with

`virtualenv myenv` or `python3 -m venv myenv`

Activate the virtual env with

`source myenv/bin/activate`

and simply deactivate it in your terminal with

`deactivate`

## Create Helloworld

With an active virtual environment run:

`pip install Django`

create then the project

`django-admin startproject hello_world_project`

and is ready to be installed and run the server

```
cd hello_world_project
python manage.py migrate
python manage.py runserver
```

Lastly create an app inside the project

` python manage.py startapp pewee`

Inspired by [Django central](https://djangocentral.com/create-a-hello-world-django-application/) and [Virtual Env](https://djangocentral.com/how-to-a-create-virtual-environment-for-python/)

## How to create a migration

Create model for the db table in `models.py` then run

`python manage.py makemigrations my_app`

To analyse the sql that would run, launch:

`python manage.py sqlmigrate my_app 0001`

To effectively apply the migration:

`python manage.py migrate`

## Migrations with Pewee as ORM

Install Pewee and pewee migrations

`pip install peewee-migrations`

`pem init` to let Pewee create the migrations.json file

`pem add my_app.models.Entity` to add the entity to the migration

`pem watch` should notify if everything went well and pewee is able to generate the migration

`pem show` shows which migration is going to run

`pem migrate` to run the migration to the db

## Start with Gunicorn

After having installed gunicorn
`python -m pip install gunicorn`

It's possible to run the same webserver through gunicorn via
`gunicorn hello_world_django.wsgi`
