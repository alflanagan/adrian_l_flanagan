#!/usr/bin/env bash
PG9CONFIG=/etc/postgresql/9.6/main/pg_hba.conf
PG10CONFIG=/etc/postgresql/10/main/pg_hba.conf

# clone auth config
sudo cp ${PG9CONFIG} ${PG10CONFIG} || exit 1
echo 'local   all             adrian_l_flanagan                       md5' >> ${PG10CONFIG}
sudo cat ${PG10CONFIG}
sudo service postgresql restart 10
whoami
ll -d adrian_l_flanagan
cd adrian_l_flanagan || exit 1
ln -s prod_settings.py settings.py
cd .. || exit 1
sudo -u postgres psql -U postgres -c "CREATE USER adrian_l_flanagan PASSWORD 'travis_test_password' CREATEDB;"
python3 -m pip install --upgrade pip
python3 -m pip install pipenv
pipenv install --three
pipenv run python manage.py migrate --noinput
pipenv run python manage.py collectstatic --noinput
