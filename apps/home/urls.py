from django.urls import path
from . import views
urlpatterns = [
 path('home',views.user_home, name="user_home"),
 path('upload',views.upload_post,name="upload_post"),
 path('update_like/<int:id>',views.update,name="update_like"),
path('update_like',views.update,name="update_like"),
]