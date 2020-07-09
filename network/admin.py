from django.contrib import admin
from network.models import User, Post, Follower, Follow, Liked

class LikedAdmin(admin.ModelAdmin):
    filter_horizontal = ("post",)

class FollowAdmin(admin.ModelAdmin):
    filter_horizontal = ("following",)

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Follower)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Liked, LikedAdmin)
