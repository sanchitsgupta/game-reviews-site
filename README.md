# Game Reviews Site

![PyPI pyversions](https://img.shields.io/github/pipenv/locked/python-version/sanchitsgupta/game-reviews-site)
![Linux](https://svgshare.com/i/Zhy.svg)
![PyPI license](https://img.shields.io/github/license/sanchitsgupta/game-reviews-site)

A simple website that supports adding game reviews, recommends new games to users, and has basic user authentication.

New games are recommended using k-means algorithm. We pre-cluster the users, and when some user asks for their recommendations, we suggest movies that are highly rated by other users in the same cluster.

## Running

1. Make sure [Python 3.10+](https://www.python.org/downloads/) is installed.
2. Install [pipenv](https://github.com/kennethreitz/pipenv).
    ```shell
    $ pip install pipenv
    ```
3. Install requirements
    ```shell
    $ pipenv install
    ```
4. Apply DB migrations and populate the DB. `setup.sh` script does this for you.
    ```shell
    $ ./setup.sh
    ```
5. Run the server
    ```
    $ pipenv run python game_site/manage.py runserver 8000
    ```
6. Visit http://127.0.0.1:8000 and start exploring.

## Acknowledgements

This code is mainly based off of Jose Dianes' [tutorial](https://www.codementor.io/@jadianes/get-started-with-django-building-recommendation-review-app-du107yb1a) on building a Wine Recommendation Site. Do check out his awesome tutorial!
