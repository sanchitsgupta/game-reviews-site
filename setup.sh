#!/bin/bash

# apply db migrations
pipenv run python game_site/manage.py makemigrations
pipenv run python game_site/manage.py migrate

# load data
pipenv run python game_site/load_users.py
pipenv run python game_site/manage.py load_data
