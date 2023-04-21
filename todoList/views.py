from django.shortcuts import render,redirect,HttpResponse
from .models import *
from .forms import *
from django.contrib.auth import login,authenticate,logout
from django.views.generic import CreateView,View,FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from .decorators import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse


class SingupView(CreateView):
    model=User
    form_class=SingupForm
    template_name="singup.html"
    success_url="/"
    def get_context_data(self,**kwargs):
        kwargs['user_type']='Public'
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        return redirect("home") 
def loginView(req):
    form =AuthenticationForm(req.POST or None)
    if req.method =="POST":
        username=req.POST.get('username')
        password=req.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(req,user)
            return redirect("home")
    return render(req,"login.html",{"form":form})
@login_required
@public_required
def homeView(req):
    form=MessageForm(req.POST or None)    
    data={
        "form":form,
        "us":User.objects.get(pk=req.user.id),
        "message":Message.objects.all()
    }
    if req.method =="POST":
        link_url = 'http://127.0.0.1:8000' + reverse(homeView)
        if form.is_valid():
            p=form.save(commit=False)
            p.user=req.user
            p.created_at=timezone.now()
            p.save()
            html_message = '<p>{{user.username}}</p><br/><p>Click <a href="{}">here</a> to go to the website.</p>'.format(link_url)
            send_mail(
                'New message from your todo list',
                f'Name: {p.user.username}\nEmail: {p.user.email}\nMessage: {p.message}\nStarting-Time:{p.created_at},\nEnd-Time:{p.end_at}\nLink:{link_url}',
                p.user.email,
                ['45636cd9b09dda'], html_message=html_message,
                fail_silently=False,
            )
            return redirect(homeView)
    return render(req,"home.html",data)

@login_required
@public_required
def logoutView(req):
    logout(req)
    return redirect("singup")
@login_required
@public_required
def delete(req,id):
    mess=Message.objects.get(pk=id)
    mess.delete()
    return redirect("home")
