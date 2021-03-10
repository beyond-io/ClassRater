#!/usr/bin/env bash 

sudo -n dnf install -y pipenv

cd /vagrant
pipenv sync --dev

# The app logs will be collected in nohup.out
nohup pipenv run python manage.py runserver 0.0.0.0:8000 &
