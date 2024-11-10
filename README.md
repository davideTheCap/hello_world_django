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

Inspired by [Django central](https://djangocentral.com/create-a-hello-world-django-application/) and [Virtual Env](https://djangocentral.com/how-to-a-create-virtual-environment-for-python/)
