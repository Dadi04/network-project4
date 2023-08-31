from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone

import json
from .models import User, NewPost, Likes

def paginator(request, mode, username):
    page_number = request.GET.get('page')
    if mode == 'all':
        posts = NewPost.objects.all().order_by('-timestamp')
    elif mode == 'following':
        # get the list of id of the people i follow
        following = User.objects.filter(username__in=request.user.following).values_list('id', flat=True)
        posts = NewPost.objects.filter(posted_by__in=following).order_by('-timestamp')
    elif mode == 'profile':
        posts = NewPost.objects.filter(posted_by=User.objects.get(username=username)).order_by('-timestamp')
    
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page_number)
    return page_obj

def index(request):
    page_obj = paginator(request, 'all', 'nothing')
    return render(request, "network/index.html", {
        "posts": page_obj
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
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
@login_required
def newpost(request):
    if request.method == "POST":
        text = request.POST['new_post']
        new_post = NewPost.objects.create(posted_by=request.user, text=text)
        new_post.save()
        likes = Likes.objects.create(liked_by=request.user, post=new_post)
        likes.save()
        return HttpResponseRedirect(reverse("index"))

@login_required    
def profile(request, username):
    page_obj = paginator(request, 'profile', username)
    # if user's profile i am trying to connect to is mine, don't show any button
    if username == request.user.username:
        follow = False
        followed = False
    # if not
    else: 
        # check if my name is in the follows list and if it is, turn on followed button
        if request.user.username in User.objects.get(username=username).followers:
            followed = True
            follow = False
        # if not
        else:
            # turn on follow button
            followed = False
            follow = True

    return render(request, "network/profile.html", {
        "user": request.user,
        "user_profile": User.objects.get(username=username),
        "posts": page_obj,
        "follow": follow,
        "followed": followed,
    })

@login_required 
def follow(request, username):
    if request.method == "POST":
        # get the info of the account i want to follow and give me it's list
        user = User.objects.get(username=username)
        # get a new follower's account
        new_follower = User.objects.get(username=request.user.username)

        # append follower to the user he is trying to follow
        user.followers.append(new_follower.username)
        user.save()
        # append his account to following on my account
        new_follower.following.append(user.username)
        new_follower.save()
        # redirect back to the same page
        return redirect(request.META.get('HTTP_REFERER', 'network/index.html'))

@login_required
def unfollow(request, username):
    if request.method == "POST":
        # get the info of the account i want to follow and give me it's list
        user = User.objects.get(username=username)
        # get a new follower's account
        new_follower = User.objects.get(username=request.user.username)

        # append follower to the user he is trying to follow
        user.followers.remove(new_follower.username)
        user.save()
        # append his account to following on my account
        new_follower.following.remove(user.username)
        new_follower.save()
        # redirect back to the same page
        return redirect(request.META.get('HTTP_REFERER', 'network/index.html'))

@login_required 
def following(request):
    page_obj = paginator(request, 'following', 'nothing')
    # get the people i follow using id's
    return render(request, "network/following.html", {
        "posts": page_obj
    })

@login_required   
def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        post = NewPost.objects.get(pk=post_id)
        post.text = data["text"]
        post.timestamp = timezone.now()
        post.save()
        return JsonResponse({"message": "Change successful", "data": data["text"]})
    else:
        return JsonResponse({"error": "POST request required."}, status=400)

@login_required    
def like(request, post_id):
    if request.method == "POST":
        post = NewPost.objects.get(pk=post_id)
        user = request.user
        if Likes.objects.filter(liked_by=user, post=post).exists():
            like = Likes.objects.get(liked_by=user, post=post)
            like.delete()
        else:
            like = Likes(liked_by=user, post=post)
            like.save()
        likes_count = post.likes.count()
        return JsonResponse({"message": "Post liked/unliked", "likes": likes_count})
    else:
        return JsonResponse({"error": "POST request required."}, status=400)