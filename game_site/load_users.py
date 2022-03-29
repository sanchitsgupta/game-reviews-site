import os
from os.path import join
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "game_site.settings")

import django
django.setup()

from django.conf import settings
from django.contrib.auth.models import User


if __name__ == "__main__":

    # NOTE: For some reason, loading users using User.objects.create_user() doesn't work when used
    # inside a django management command class. The user is created but without any password. That is why
    # I have written this script specially to load some users.

    path = join(settings.BASE_DIR, 'reviews', 'data', 'users.csv')
    df = pd.read_csv(path)
    data = df.to_dict(orient='records')
    for item in data:
        User.objects.create_user(username=item['username'], password='gamereview@123')

    print(f'Successfully loaded {len(data)} users.')
