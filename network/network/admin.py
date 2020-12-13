from django.contrib import admin

# Register your models here.

from network.models import User, Posts, FollowerData, LikedData

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "password", "followers", "following")
    list_editable = ("username", "email", "password", "followers", "following")

class PostsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post_text", "post_date", "post_likes")
    list_display_links = ("user", "post_likes")
    list_editable = ("post_text", "post_date")
    

class FollowerDataAdmin(admin.ModelAdmin):
    list_display = ("id", "followed", "following", "user")
    list_display_links = ("followed", "following", "user")

class LikedDataAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "likedPost")
    list_display_links = ("user", "likedPost")


# Register your models here.
admin.register(User),
admin.register(Posts),
admin.register(FollowerData),
admin.register(LikedData)

admin.site.register(User, UserAdmin),
admin.site.register(Posts, PostsAdmin),
admin.site.register(FollowerData, FollowerDataAdmin),
admin.site.register(LikedData, LikedDataAdmin)