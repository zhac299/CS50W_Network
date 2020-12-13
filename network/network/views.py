from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import User, Posts, FollowerData, LikedData


# Returns the index page
def index(request):
    post_objects = Posts.objects.all()
    paginator = Paginator(post_objects, 10)
    totalPages = paginator.num_pages
    page_number = request.GET.get('page')    
    page_obj = paginator.get_page(page_number)
    pageList = []
    for i in range(0, totalPages):
        pageList.append(i)    
    
    pageNum = page_obj.number

    if request.method == "POST":
        postData = Posts()
        postData.user = request.user
        postData.post_text = request.POST["postContent"]
        postData.post_likes = 0
        postData.post_date = timezone.now()
        postData.save()
        return render(request, "network/index.html", {
            "info": "Post Submitted",
            "totalPages": totalPages,
            'page_obj': page_obj
        })
    else:
        return render(request, "network/index.html", {
            "totalPages": totalPages,
            'page_obj': page_obj
        })


# JS function for editing posts
@login_required
@csrf_exempt
def edit(request, post_id):
    post_objects = Posts.objects.filter(id = post_id)
    
    updatePost = Posts.objects.get(id = post_id)

    if request.method == "PUT":
        data = json.loads(request.post_text)
        print(data)
        updatePost.post_text = data
        updatePost.save()
        return HttpResponse(status=204)


    return JsonResponse([post_object.serialize() for post_object in post_objects], safe=False)

@login_required
@csrf_exempt
def editChange(request, post_id):
    updatePost = Posts.objects.get(id = post_id)

    if request.method == "PUT":
        data = json.loads(request.body)
        updatePost.post_text = data["post_text"]
        updatePost.save()
        return HttpResponse(status=204)



@login_required
@csrf_exempt
def likeChange(request, post_id):
    thePost = Posts.objects.get(id = post_id)
    like = LikedData()

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    print(data)
    try:
        user = User.objects.get(username = request.user.username)
    except User.DoesNotExist:
        return JsonResponse({
            "error": f"User with username {request.user.username} does not exist."
        }, status=400)


    if (not LikedData.objects.filter(user = user, likedPost = thePost).exists()):
        like.user = user
        like.likedPost = thePost
        like.save()
        thePost.post_likes += 1
        thePost.save()
        cursor.close()
    else:
        return JsonResponse({"messge": "You have already liked this post"}, status=400)

    return JsonResponse({"message": "Post Liked."}, status=201)


@login_required
@csrf_exempt
def unlikeChange(request, post_id):
    thePost = Posts.objects.get(id = post_id)
    like = LikedData()

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    print(data)
    try:
        user = User.objects.get(username = request.user.username)
    except User.DoesNotExist:
        return JsonResponse({
            "error": f"User with username {request.user.username} does not exist."
        }, status=400)


    if (LikedData.objects.filter(user = user, likedPost = thePost).exists()):
        LikedData.objects.filter(user = user, likedPost = thePost).delete()
        thePost.post_likes -= 1
        thePost.save()
        cursor.close()
    else:
        return JsonResponse({"messge": "You haven't liked this post"}, status=400)

    return JsonResponse({"message": "Post UnLiked."}, status=201)


# JS function for index
@login_required
def allPostDisplay(request, pageNumber):
    postObj = Posts.objects.all()
    paginator = Paginator(postObj, 10)
    totalPages = paginator.num_pages
    current_page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(current_page_number)

    pageNum = (page_obj.number)

    if (pageNumber != 1):        
        numOfObjectsMax = pageNum * 10
        numOfObjectsLow = numOfObjectsMax - 10        
        step1 = paginator.page(pageNumber)
        postObj = step1.object_list

        return JsonResponse([post_object.serialize() for post_object in postObj], safe=False)        
    elif pageNumber == 1:
        step1 = paginator.page(pageNumber)
        post_objects_list = step1.object_list
        return JsonResponse([post_object.serialize() for post_object in post_objects_list], safe=False)



# Returns the profile page
@login_required
@csrf_exempt
def profile(request, usersname):
    post_objects = Posts.objects.filter(user = request.user)
    paginator = Paginator(post_objects, 10)
    totalPages = paginator.num_pages
    page_number = request.GET.get('page')    
    page_obj = paginator.get_page(page_number)
    pageList = []
    for i in range(0, totalPages):
        pageList.append(i)    
    
    pageNum = page_obj.number

    if "followButton" in request.POST:
        new_following = User.objects.get(username = usersname)
        currentLogged = request.user
        
        newFollower = FollowerData()
        newFollower.followed = currentLogged
        newFollower.following = new_following
        newFollower.user = new_following
        newFollower.save()

        new_following2 = User.objects.get(username = usersname)
        new_following2.followers += 1
        new_following2.save()
        currentLogged2 = User.objects.get(username = request.user.username)
        currentLogged2.following += 1
        currentLogged2.save()


        return render(request, "network/profile.html", {
            "usersname": usersname,
            "followConfirm": 1,
            "totalPages": pageList,
            'page_obj': page_obj
        })

    if 'UnfollowButton' in request.POST:
        remove_new_following = User.objects.get(username = usersname)
        removeFollower = FollowerData.objects.filter(followed = request.user, following = remove_new_following).delete()


        new_following2 = User.objects.get(username = usersname)
        new_following2.followers -= 1
        new_following2.save()
        currentLogged2 = User.objects.get(username = request.user.username)
        currentLogged2.following -= 1
        currentLogged2.save()


    user_following = User.objects.get(username = usersname)
    currentLogged = request.user
    followCheck = FollowerData.objects.filter(followed = currentLogged, following = user_following)
    if followCheck:
        return render(request, "network/profile.html", {
            "usersname": usersname,
            "followConfirm": 1,
            "totalPages": pageList,
            'page_obj': page_obj
        })

    return render(request, "network/profile.html", {
        "usersname": usersname,
        "totalPages": pageList,
        'page_obj': page_obj
    })


# JS function for profile
@login_required
def loadUser(request, user_name):
    # Get Username
    user_data = User.objects.filter(username = user_name)

    # Return data in reverse chronological order as a JSON object
    return JsonResponse([user_info.serialize() for user_info in user_data], safe=False)


# JS function to get posts in chronological order
@login_required
def getUserPosts(request, user_name, pageNumber):
    # Get the User based on their username
    theUser = User.objects.get(username = user_name)

    postObj = Posts.objects.filter(user = theUser).order_by('-post_date').all()
    paginator = Paginator(postObj, 10)
    totalPages = paginator.num_pages
    current_page_number = request.GET.get('page')
    page_obj = paginator.get_page(current_page_number)

    pageNum = (page_obj.number)


    if (pageNumber != 1):        
        numOfObjectsMax = pageNum * 10
        numOfObjectsLow = numOfObjectsMax - 10        
        step1 = paginator.page(pageNumber)
        postObj = step1.object_list

        return JsonResponse([post_object.serialize() for post_object in postObj], safe=False)        
    elif pageNumber == 1:
        step1 = paginator.page(pageNum)
        post_objects_list = step1.object_list
        return JsonResponse([post_object.serialize() for post_object in post_objects_list], safe=False)


@login_required
def getUserInfo(request, user_name):
    # Get the User based on their username
    theUser = User.objects.filter(username = user_name)
    return JsonResponse([user_post.serialize() for user_post in theUser], safe=False)


# Returns the following page
@login_required
def following(request, user):
    followingData = FollowerData.objects.filter(followed = request.user)  
    followers_list = []
    followingPosts = Posts()
    followingList = []

    for item in followingData:   
        followers_list.append(item.following)

    for followers in followers_list:
        followingPosts = Posts.objects.filter(user = followers)
        followingList += list(followingPosts)


    paginator = Paginator(followingList, 10)
    totalPages = paginator.num_pages
    current_page_number = request.GET.get('page')
    page_obj = paginator.get_page(current_page_number)

    pageNum = (page_obj.number)


    return render(request, "network/index.html", {
        "val": 1,
        "totalPages": totalPages,
        'page_obj': page_obj
    })


# JS function to get followers posts
@login_required
def getFollowingPost(request, pageNumber):
    followingData = FollowerData.objects.filter(followed = request.user)  
    followers_list = []
    followingPosts = Posts()
    followingList = []

    for item in followingData:   
        followers_list.append(item.following)

    for followers in followers_list:
        followingPosts = Posts.objects.filter(user = followers)
        followingList += list(followingPosts)


    paginator = Paginator(followingList, 10)
    totalPages = paginator.num_pages
    current_page_number = request.GET.get('page')
    page_obj = paginator.get_page(current_page_number)

    pageNum = (page_obj.number)


    print(len(followingList))
    print(page_obj.paginator.num_pages)

    if (pageNumber != 1):        
        step1 = paginator.page(pageNumber)
        postObj = step1.object_list
        return JsonResponse([post_object.serialize() for post_object in postObj], safe=False)        
    elif (pageNumber == 1):
        step1 = paginator.page(pageNumber)
        post_objects_list = step1.object_list
        return JsonResponse([post_object.serialize() for post_object in post_objects_list], safe=False)



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
