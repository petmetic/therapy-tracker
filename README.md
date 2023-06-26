# THERAPY TRACKER

## About
Therapy Tracker is an app that helps you keep your client's therapy history up to date.

## First steps
1. Clone or fork the repo. Make sure you have the local settings folder!
2. Install virtual environment for python 3.11
3. Install requirements.txt: `pip install -r requirements.txt`
4. Create database:
   - run `./manage.py migrate`

5. Create admin superuser: run `./manage.py createsuperuser`
6. To run the application locally, got into `src` folder and run `./manage.py runserver` in your terminal.
7. To run the tests, got into `src` folder , run `./manage.py test web` in your terminal.
8. To run sync, run `./manage.py sync` in your terminal.
9. To set up translation:
   - run `django-admin makemessages -l sl`
   - run `django-admin compilemessages -l sl`
