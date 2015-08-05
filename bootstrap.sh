# SETUP FOR VAGRANT DEV BOX CRAWLER

$PROJNAME=buzzhire
# GENERAL SETUP
sudo apt-get update
sudo apt-get -y install vim
sudo apt-get -y install curl

#PYTHON / DJANGO
sudo apt-get -y install python-pip
sudo apt-get -y install python-dev

# POSTGRES & DEPENDENCIES
sudo apt-get -y install postgresql
sudo apt-get -y postgresql-9.1-postgis
sudo apt-get -y install python-software-properties
sudo apt-add-repository ppa:ubuntugis/ppa
sudo apt-get -y update
sudo apt-get -y install postgresql-9.1-postgis
sudo apt-get -y install libpq-dev
sudo apt-get -y install libffi-dev
sudo apt-get -y install libgeos-dev

# DB SETUP 
sudo su postgres -c "createuser -d -R -P $PROJNAME"
sudo su postgres -c "createdb -O $PROJNAME $PROJNAME"
sudo su postgres -c "psql $PROJNAME -c 'CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;'"
sudo /etc/init.d/postgresql restart

# PIP REQUIREMENTS
cd /vagrant
sudo pip install -r requirements.pip

# SECRET FILE SETUP
touch /vagrant/settings/secret.py
echo "DEFAULT_DATABASE_HOST = 'localhost'" >> /vagrant/settings/secret.py
echo "DEFAULT_DATABASE_NAME = '$PROJNAME'" >> /vagrant/settings/secret.py
echo "DEFAULT_DATABASE_USER = '$PROJNAME'" >> /vagrant/settings/secret.py
echo "DEFAULT_DATABASE_PASSWORD = '$PROJNAME'" >> /vagrant/settings/secret.py
echo "SECRET_KEY = 'Km)lid2fmzVy0^wJUfi60mAP5NeVK'" >> /vagrant/settings/secret.py
echo "EMAIL_HOST_PASSWORD = 'asdf'" >> /vagrant/settings/secret.py
echo "AWS_SECRET_ACCESS_KEY = 'xxx'" >> /vagrant/settings/secret.py
echo "BRAINTREE_PRIVATE_KEY = 'yyy'" >> /vagrant/settings/secret.py

mkdir -p /vagrant/logs/

echo 'export DJANGO_CONFIGURATION="VagrantDev"' >> ~/.profile
cd /vagrant; ./manage.py runserver 0.0.0.0:8000
