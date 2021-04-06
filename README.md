# swapp_project
SwApp is a web app built using the Django framework. It helps with organization and management of events as markets, fairs or exchanges.

## Deployment in a local development environment
To deplot SwApp in a local environment, follow these seps:
1. git clone
2. install django 2.2 and python 3
3. `pip install -r requirements.py`
4. `cd /path/to/local/repo/swapp_project/`
5. `python manage.py makemigrations` to auto-generate migrations
6. `python manage.py migrate` to create the database and the necessary tables
7. `python populate_swapp.py` to populate the database
8. `python manage.py runserver` to run the local development server
9. enjoy!

For convenience, there is a default event provided and a default superuser with the credentials admin/admin. We strongly advise everyone to use the django admin interface to edit these. 
