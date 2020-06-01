from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View 
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from apps.core.forms import Form_Login,User_master_form,User_detail_form
from apps.core.models import Account_detail
# Create your views here.
class Loginview(View):
    def get(self,request):
      form_login= Form_Login()
      return render(request, 'loginpage.html', {"form_login": form_login})
    def post(self,request):
       form_data=Form_Login(request.POST)
       if form_data.is_valid():
            username=form_data.cleaned_data.get('username')
            password=form_data.cleaned_data.get('password')
            user = authenticate(email=username, password=password)
            if user == None:
                messages.error(request, 'Incorrect Username or Password')
                return self.get(request)
            else:
                request.session['USER_EMAIL'] = user.email
                request.session['IS_SUPER_USER'] = user.is_superuser
                try:
                   user_detail=Account_detail.objects.get(Account_id=user.id)
                   request.session['USER_ID']=user_detail.id
                except Exception as e:
                    return HttpResponse(e)
                request.session['USER_NAME'] = user_detail.user_first_name
                return redirect("user_home")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup(request,id=None):
    if id:
        User = get_user_model()
        user_detail_obj=Account_detail.objects.get(id=id)
        user_obj = User.objects.get(id=user_detail_obj.Account_id)
        form_user_master=User_master_form(request.POST or None,instance=user_obj)
        form_user_detail=User_detail_form(request.POST or None,instance=user_detail_obj)
    else:
        form_user_master=User_master_form(request.POST or None)
        form_user_detail=User_detail_form(request.POST or None)
    if form_user_master.is_valid() and form_user_detail.is_valid():
        account_obj = form_user_master.save(commit=False)
        if not id:
            account_obj.is_active = True
            account_obj.password_reset = True
            account_obj.type_of_user = 2
            account_obj.set_password(form_user_master.cleaned_data.get('password'))
        account_obj.save()
        account_detail_obj = form_user_detail.save(commit=False)
        account_detail_obj.Account = account_obj
        account_detail_obj.save()
        if not id:
            messages.success(request, 'Please login to continue')
            return redirect('Renders Login Page')
        else:
             messages.success(request, 'updated')
             return redirect("user_home")

    return render(request, 'add_user.html', {"form_user_master":form_user_master,"form_user_detail":form_user_detail})

