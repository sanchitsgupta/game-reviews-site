from os.path import join

from django.core.management.base import BaseCommand
from django.conf import settings
import pandas as pd

from reviews.models import Game, Review


def save_data(csvpath, Model):
    df = pd.read_csv(csvpath)
    data = df.to_dict(orient='records')

    model_data = [Model(**item) for item in data]
    Model.objects.bulk_create(model_data)

    return len(data)


def save_reviews(csvpath):
    df = pd.read_csv(csvpath)
    data = df.to_dict(orient='records')

    updated_data = []
    for item in data:
        updated_item = {**item, 'game': Game.objects.get(id=item['game_id'])}
        updated_item.pop('game_id')
        updated_data.append(Review(**updated_item))

    Review.objects.bulk_create(updated_data)
    return len(updated_data)


class Command(BaseCommand):
    help = 'Loads some data into the DB'

    def handle(self, *args, **options):
        data_dir = join(settings.BASE_DIR, 'reviews', 'data')

        no_games = save_data(join(data_dir, 'games.csv'), Game)
        no_reviews = save_reviews(join(data_dir, 'reviews.csv'))

        self.stdout.write(self.style.SUCCESS(
            f'Successfully loaded {no_games} games and {no_reviews} reviews.')
        )
