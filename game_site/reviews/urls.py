from django.urls import re_path
from . import views


urlpatterns = [
    # ex: /
    re_path(r'^$', views.review_list, name='review_list'),

    # ex: /review/5/
    re_path(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail'),

    # ex: /game/
    re_path(r'^game$', views.game_list, name='game_list'),

    # ex: /game/5/
    re_path(r'^game/(?P<game_id>[0-9]+)/$', views.game_detail, name='game_detail'),
    re_path(r'^game/(?P<game_id>[0-9]+)/add_review/$', views.add_review, name='add_review'),

    # ex: /review/user - get reviews for the logged user
    re_path(r'^review/user/(?P<username>\w+)/$', views.user_review_list, name='user_review_list'),

    # ex: /review/user - get reviews for the user passed in the url
    re_path(r'^review/user/$', views.user_review_list, name='user_review_list'),

    # ex: /recommendation - get wine recommendations for the logged user
    re_path(r'^recommendation/$', views.user_recommendation_list, name='user_recommendation_list'),
]
