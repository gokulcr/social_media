from django.db import models
from django.conf import settings
from apps.core.models import Account_detail
# Create your models here.
class User_post(models.Model):
    created_by=models.ForeignKey(Account_detail, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/',null=True,blank=True)
    description=models.TextField(max_length=400,null=True)
    status= models.SmallIntegerField(null=True)
    created_date=models.DateTimeField(auto_now_add=True)
    edit_date=models.DateTimeField(auto_now_add=True)
    like_count=models.IntegerField(default=0)
    class Meta:
        db_table  = settings.TABLE_PREFIX+'user_post'
    def __str__(self):
        return self.description
class Post_like(models.Model):
    user_post=models.ForeignKey(User_post, on_delete=models.CASCADE)
    liked_by=models.ForeignKey(Account_detail, on_delete=models.CASCADE)
    status= models.SmallIntegerField(null=True)
    class Meta:
        db_table  = settings.TABLE_PREFIX+'post_like'
    def __str__(self):
        return self.status
