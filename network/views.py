from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Post, Liked, Follow, Follower
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):

    post_list = Post.objects.all().order_by('-id')
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        liked = Liked.objects.get(name=request.user)
        likedlist = liked.post.all().order_by('-id')
        return render(request, "network/index.html", {
            "posts": posts,
            "liked": likedlist
        })

    return render(request, "network/index.html", {
        "posts": posts,
        
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            liked = Liked.objects.create(name = user)
            liked.save()
            follow = Follow.objects.create(name = user)
            follow.save()
            follower = Follower.objects.create(name = user)
            follower.save()

        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profile(request, username):
    user = User.objects.get(username = username)
    post_list = Post.objects.all().filter(user = user.id).order_by('-id')

    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    follower = Follower.objects.get(name=user)
    followersCount = follower.followers.count()

    following = Follow.objects.get(name=user)
    followingCount = following.following.count()

    if request.user.is_authenticated:
        
        # follower = Follower.objects.get(name=user)
        # followersCount = follower.followers.count()

        # following = Follow.objects.get(name=user)
        # followingCount = following.following.count()
    
        follow = Follow.objects.get(name=request.user)
        followed = follow.following.all()

        liked = Liked.objects.get(name=request.user)
        likedlist = liked.post.all().order_by('-id')
        return render(request, "network/profile.html", {
            "username": user,
            "posts": posts,
            "liked": likedlist,
            "followed": followed,
            "followersCount": followersCount,
            "followingCount": followingCount
        })
    
    else:
        return render(request, "network/profile.html", {
            "username": user,
            "posts": posts,
            "followersCount": followersCount,
            "followingCount": followingCount
        })

def post(request):

    if request.method == "POST":

        form = request.POST
        user = request.user
        content = form["content"]
        newPost = Post.objects.create(
            user = user,
            content = content,
        )
        newPost.save()
        print("Success")
        return HttpResponseRedirect(reverse("index"))
        
    else:
        print("error")
        return HttpResponseRedirect(reverse("index"))

def likes(request, id):
    
    liked = Liked.objects.get(name=request.user)
    post = Post.objects.get(id=id)

    liked.post.add(post)
    post.likes += 1;
    post.save()
    print(post.likes)
    return HttpResponse('')
    
def dislikes(request, id):

    liked = Liked.objects.get(name=request.user)
    post = Post.objects.get(id=id)
    liked.post.remove(post)
    post.likes -= 1;
    post.save()
    print(post.likes)
    return HttpResponse('')

def follow(request, username):

    follow = Follow.objects.get(name=request.user)
    user = User.objects.get(username=username)
    follower = Follower.objects.get(name=user) 

    if user not in follow.following.all():
        follow.following.add(user)
        follow.save()
        
        follower.followers.add(request.user)
        follower.save()
    else:
        print("Error")
    
    return HttpResponse('')

def unfollow(request, username):

    follow = Follow.objects.get(name=request.user)
    user = User.objects.get(username=username)

    follower = Follower.objects.get(name=user)

    if user in follow.following.all():
        follow.following.remove(user)
        follow.save()
        follower.followers.remove(request.user)
        follower.save()
    else:
        print("Error")

    return HttpResponse('')
    
def following(request):
    
    posts = Post.objects.all().order_by('-id')

    follow = Follow.objects.get(name=request.user)
    followed = follow.following.all()

    liked = Liked.objects.get(name=request.user)
    likedlist = liked.post.all().order_by('-id')

    postlist = []

    for post in posts:
        for following in followed:
            if post.user == following:
                postlist.append(post)
                continue
    
    page = request.GET.get('page', 1)

    paginator = Paginator(postlist, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "network/following.html", {
            "posts": posts,
            "liked": likedlist
        })

def save(request, id, data):
    post = Post.objects.get(id=id)
    if request.user == post.user:
        print( "Old data: " + str(post.content))
        post.content = data
        post.save()
        print( "New data: " + str(post.content))
        return HttpResponse('')
    else:
        print("Error, You can't edit that!")
        return HttpResponse('')
