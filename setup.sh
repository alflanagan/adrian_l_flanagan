#!/usr/bin/env bash

# clone auth config (might need to fix source path for another version)
sudo cp /etc/postgresql/9.6/main/pg_hba.conf /etc/postgresql/10/main/pg_hba.conf

cd adrian_l_flanagan || exit 1
ln -s prod_settings.py settings.py
cd .. || exit 1
psql -U postgres -c "CREATE USER adrian_l_flanagan PASSWORD 'travis_test_password' CREATEDB;"
python3 -m pip install pipenv
pipenv install --three
pipenv run python manage.py migrate --noinput
pipenv run python manage.py collectstatic --noinput
