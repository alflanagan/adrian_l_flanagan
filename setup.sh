#!/usr/bin/env bash

ln -s adrian_l_flanagan/prod_settings.py settings.py
pip install pipenv
pipenv install
python manage.py migrate
