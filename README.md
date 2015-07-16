BuzzHire
========

Local development
-----------------

### Installation

1. Check out code and `git checkout develop`.
2. Ensure Postgres and Postgis are installed, and create a database:
   
        $ SITENAME=buzzhire
        $ sudo su postgres -c "createuser -d -R -P $SITENAME"
        $ sudo su postgres -c "createdb -O $SITENAME $SITENAME"
        $ sudo su postgres -c "psql $SITENAME -c 'CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;'"

3. Install redis, if it isn't already.
4. Create virtualenv and run `pip install -r requirements.pip`.
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
3. `./manage.py runserver`
4. In another terminal, run `workon buzzhire` and then `./manage.py run_huey`.
   (This is the task queue.)
5. The site should now be accessible at `http://localhost:8000`.

N.B. If there are new code commits from other developers, you may need to run
the following commands before `./manage.py runserver`:

1. `pip install -r requirements.txt`
2. `./manage.py migrate`

## Committing and deploying code

In general, code should be committed to the `develop` branch.

### Deployment using Fabric

Before deploying, ensure Fabric is installed on your system.  You will also
need to ask for your public keys to be added to the BuzzHire server.

Your deployment process is then simply:

1. `git push` your code to the `develop` branch.
2. `fab deploy`. 

## Front end development

### Templates

Django uses a template system.  Documentation is here: https://docs.djangoproject.com/en/1.8/ref/templates/language/

The templates you will be editing are under the `templates` directory.

### Static files

To include static files such as CSS, static images and javascript,
use the `{% static %}`  template tag.  This will look under the `static`
directory for the files.  Examples in `templates/include/html_head.html`.  

The main stylesheet is at `static/css/main.less`, and the main javascript file
is at `static/js/theme.js`.

### Compression and LESS

Some static files are automatically compressed, and LESS files compiled,
using a tool called Django-compressor.  An example of this in action
is in `templates/include/html_head.html`.  

### Adding third party files using Bower

1. Edit `settings/project.py` and find the line `BOWER_INSTALLED_APPS`.  Add
   the third party source to it.
2. Run `./manage.py bower install` locally.  This will collect the third party
   source into `components/bower_components`.
3. Anything within `components/bower_components` can now be included in
   templates using the `{% static %}` template tag.  For examples,
   see `templates/include/html_head.html`.
