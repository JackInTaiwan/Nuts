from django.urls import path
import User.views



urlpatterns = [
    path("add", User.views.add_user),
    path("dump", User.views.dump_users),
    path("vote", User.views.vote_weather),
]