#!/usr/bin/env bash

cd adrian_l_flanagan || exit 1
ln -s prod_settings.py settings.py
cd .. || exit 1
python3 -m pip install pipenv
pipenv install --three
pipenv run python manage.py migrate --noinput
pipenv run python manage.py collectstatic --noinput
