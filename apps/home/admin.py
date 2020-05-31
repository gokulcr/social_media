from django.contrib import admin
from apps.home.models import User_post,Post_like
# Register your models here.

admin.site.register(User_post)
admin.site.register(Post_like)