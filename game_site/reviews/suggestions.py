from django.contrib.auth.models import User
import numpy as np
from sklearn.cluster import KMeans
from scipy.sparse import dok_matrix

from .models import Review, Cluster


def update_clusters():

    num_reviews = Review.objects.count()

    if num_reviews > 10:

        # Create a sparse matrix from user reviews
        all_user_names = list(map(lambda x: x.username, User.objects.only("username")))
        all_game_ids = set(map(lambda x: x.game.id, Review.objects.only("game")))
        num_users = len(all_user_names)
        ratings_m = dok_matrix((num_users, max(all_game_ids)+1), dtype=np.float32)
        for i in range(num_users): # each user corresponds to a row, in the order of all_user_names
            user_reviews = Review.objects.filter(user_name=all_user_names[i])
            for user_review in user_reviews:
                ratings_m[i,user_review.game.id] = user_review.rating

        # Perform kmeans clustering
        k = int(num_users / 10) + 2
        kmeans = KMeans(n_clusters=k)
        clustering = kmeans.fit(ratings_m.tocsr())

        # Update clusters
        Cluster.objects.all().delete()
        new_clusters = {i: Cluster(name=i) for i in range(k)}
        for cluster in new_clusters.values(): # clusters need to be saved before refering to users
            cluster.save()
        for i,cluster_label in enumerate(clustering.labels_):
            new_clusters[cluster_label].users.add(User.objects.get(username=all_user_names[i]))
