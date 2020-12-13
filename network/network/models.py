from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "followers": self.followers,
            "following": self.following
        }

class Posts(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    post_text = models.TextField(blank=False)
    post_date = models.DateTimeField()
    post_likes = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "postText": self.post_text,
            "timestamp": self.post_date.strftime("%b %-d %Y, %-I:%M %p"),
            "postLikes": self.post_likes
        }


class FollowerData(models.Model):
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="FollowingMe")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="IFollow")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="UserField")

    def serialize(self):
        return {
            "id": self.id,
            "followed": self.followed,
            "following": self.following,
            "User": self.User
        }

class LikedData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likedPost = models.ForeignKey(Posts, on_delete=models.CASCADE)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "likedPost": self.likedPost
        }