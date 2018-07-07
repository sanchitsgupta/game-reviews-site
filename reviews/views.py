from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import ReviewForm
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .suggestions import update_clusters

# Create your views here.

from .models import Game, Review, Cluster

def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'reviews/review_list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/review_detail.html', {'review': review})


def game_list(request):
    game_list = Game.objects.order_by('-name')
    context = {'game_list':game_list}
    return render(request, 'reviews/game_list.html', context)


def game_detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    form = ReviewForm()
    return render(request, 'reviews/game_detail.html', {'game': game, 'form': form})

@login_required
def add_review(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = request.user.username
        review = Review()
        review.game = game
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        update_clusters()
        return HttpResponseRedirect(reverse('reviews:game_detail', args=(game.id,)))

    return render(request, 'reviews/game_detail.html', {'game': game, 'form': form})

def user_review_list(request, username=None):
	if not username:
	    username = request.user.username
	latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
	context = {'latest_review_list':latest_review_list, 'username':username}
	return render(request, 'reviews/user_review_list.html', context)

@login_required
def user_recommendation_list(request):
    # get this user reviews
    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('game')
    # from the reviews, get a set of game IDs
    user_reviews_game_ids = set(map(lambda x: x.game.id, user_reviews))

    # get request user cluster name (just the first one right now)
    try:
    	user_cluster_name = User.objects.get(username=request.user.username).cluster_set.first().name
    except:
    	update_clusters()
    	user_cluster_name = User.objects.get(username=request.user.username).cluster_set.first().name

    # get usernames for other memebers of the cluster
    user_cluster_other_members = Cluster.objects.get(name=user_cluster_name).users.exclude(username=request.user.username).all()
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

	# get reviews by those users, excluding games reviewed by the request user
    other_users_reviews = Review.objects.filter(user_name__in=other_members_usernames).exclude(game__id__in=user_reviews_game_ids)
    other_users_reviews_game_ids = set(map(lambda x: x.game.id, other_users_reviews))

    # then get a game list including the previous IDs, order by rating
    game_list = sorted( list(Game.objects.filter(id__in=other_users_reviews_game_ids)), key=lambda x: x.name, reverse=True)

    # game_list = Game.objects.exclude(id__in=user_reviews_game_ids)
    return render(request, 'reviews/user_recommendation_list.html', {'username': request.user.username,'game_list': game_list})

