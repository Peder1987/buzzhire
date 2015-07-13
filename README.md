Buzzhire
========

Local development
-----------------

### Installation

1. Check out code and `git checkout develop`.
2. Create virtualenv and run `pip install -r requirements.pip`.
3. Create a database (preferably Postgres).
4. Install redis, if it isn't already.
5. The site uses django-configurations to handle settings.  The simplest thing
   way to get the site running is to configure your local machine to use the
   same settings as the `Local` settings class in `settings/installations.py`.
   However, if you want to adjust these then you should add an extra settings
   class to `installations.py`, and make sure the `DJANGO_CONFIGURATION`
   environment variable is set to the name of your class.
6. Sensitive settings should be put in `settings/secret.py`, which will not
   be under version control.  These are the minimum settings:  
        DEFAULT_DATABASE_PASSWORD = '' # Password to local database
        SECRET_KEY = '' # Any random string
7. Ensure the site can send emails - this can be done by configuring the
   configuration you're using to send via an SMTP server, or by switching
   the `EMAIL_BACKEND` to `'django.core.mail.backends.console.EmailBackend'`.
   If you're using an SMTP server, `EMAIL_HOST_PASSWORD` should be included
   in `secret.py`.
8. Set up a Braintree sandbox account and add the settings to your
   configuration class, and `BRAINTREE_PRIVATE_KEY` to `secret.py`.
9. Run `./manage.py migrate`.

 
### Running the site

1. `cd path/to/site`
2. `workon buzzhire` (Or whatever your virtualenv is called.)
2. `./manage.py runserver`
3. In another terminal, run `workon buzzhire` and then `./manage.py run_huey`.
   (This is the task queue.)
4. The site should now be accessible at `http://localhost:8000`.