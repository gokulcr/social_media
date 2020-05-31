from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
import json
from apps.home.models import User_post,Post_like
from apps.home.forms import uploadForm

def upload_post(request):
    form_data=uploadForm(request.POST,request.FILES)
    if form_data.is_valid():
        upload_obj=form_data.save(commit=False)
        upload_obj.created_by_id=request.session['USER_ID']
        upload_obj.save()
        messages.success(request, 'Posted successfully') 
        return redirect('user_home')
def user_home(request):
    upload_form=uploadForm()
    query="SELECT up.*,pl.liked_by_id FROM  Social_user_post AS up LEFT JOIN Social_post_like AS pl ON pl.user_post_id=up.id AND pl.liked_by_id={} order by up.id desc"
    query=query.format(request.session['USER_ID'])
    posts_data=User_post.objects.raw(query)
    return render(request,'user_home.html',{'form_upload':upload_form,"user_posts":posts_data})
def update(request,id):
    like_obj=Post_like()
    try:
        like_obj=Post_like.objects.get(user_post_id=id,liked_by_id=request.session['USER_ID'])
        like_obj.delete()
        like_status=0
    except:
         like_obj.user_post_id=id
         like_obj.liked_by_id=request.session['USER_ID']
         like_obj.save()
         like_status=1
    post_obj=User_post.objects.get(id=id)
    post_like_count=Post_like.objects.filter(user_post_id=id).count()
    post_obj.like_count=post_like_count
    post_obj.save()
    data=[
        {
      "post_id":id,
      "count": post_like_count,
      "like_status":like_status,
        }
    ]
    return HttpResponse(json.dumps(data))
