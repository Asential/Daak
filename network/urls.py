
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<username>", views.profile, name="profile"),
    path("post", views.post, name="post"),
    path("following", views.following, name="following"),


    path("follow/<username>", views.follow, name="follow"),    
    path("unfollow/<username>", views.unfollow, name="unfollow"),

    path("save/<int:id>/<data>", views.save, name="save"),

    path("likes/<int:id>", views.likes, name="likes"),
    path("dislikes/<int:id>", views.dislikes, name="dislikes")
    
]
