#!/usr/bin/env bash
PG9CONFIG=/etc/postgresql/9.6/main/pg_hba.conf
PG10CONFIG=/etc/postgresql/10/main/pg_hba.conf

# clone auth config
sudo cp ${PG9CONFIG} ${PG10CONFIG} || exit 1
sudo service postgresql restart 10

# create test user
sudo -u postgres psql -U postgres -c "CREATE USER adrian_l_flanagan PASSWORD 'travis_test_password' CREATEDB;"

# setup pipenv and install dependencies
python3 -m pip install --upgrade pip
python3 -m pip install pipenv
pipenv install --three

# setup django environment
ln -s prod_settings.py adrian_l_flanagan/settings.py
pipenv run python manage.py migrate --noinput
pipenv run python manage.py collectstatic --noinput
