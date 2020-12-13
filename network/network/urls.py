from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("#/<str:usersname>", views.profile, name="profile"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("#/following/<str:user>", views.following, name="following"),

    # API Routes
    path("loadPostContent/<int:pageNumber>", views.allPostDisplay, name="allPostDisplay"),
    path("getUserData/<str:user_name>", views.loadUser, name="loadUser"),
    path("getUserPost/<str:user_name>/<int:pageNumber>", views.getUserPosts, name="getUserPosts"),
    path("getUserInfor/<str:user_name>", views.getUserInfo, name="getUserInfo"),
    path("getFollowerPosts/<int:pageNumber>", views.getFollowingPost, name="getFollowingPost"),
    path("editPost/<int:post_id>", views.edit, name="edit"),
    path("editUpdate/<int:post_id>", views.editChange, name="editChange"),
    path("likeUpdate/<int:post_id>", views.likeChange, name="likeChange"),
    path("unlikeUpdate/<int:post_id>", views.unlikeChange, name="unlikeChange")

]
