from django.contrib import admin
from network.models import User, Post, Follower, Follow, Liked

class LikedAdmin(admin.ModelAdmin):
    filter_horizontal = ("post",)

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Follower)
admin.site.register(Follow)
admin.site.register(Liked, LikedAdmin)
