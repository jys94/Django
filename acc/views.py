from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User

def index(request):
    return render(request,'acc/index.html')
# Create your views here.

def login_user(request):
    if request.method == "POST" :
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        u = authenticate(username=un, password=up)
        if u : 
            login(request,u) 
            return redirect("acc:index")

    return render(request,'acc/login.html')

def logout_user(request):
    logout(request)  
    return redirect("acc:index")

def profile(request):
    return render(request, "acc/profile.html")

def delete(request):
    request.user.delete()
    return redirect("acc:index") 

def signup(request):
    if request.method=="POST":
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        ue = request.POST.get("umail")
        uf = request.POST.get("fname")
        ul = request.POST.get("lname")
        User.objects.create_user(username=un, password=up, email=ue,
        first_name=uf, last_name=ul)
        return redirect("acc:index")
    return render(request,"acc/signup.html")       

def update(request):
    if request.method=="POST":
        u = request.user
        un = request.POST.get("uname") 
        ue = request.POST.get("umail")
        uf = request.POST.get("fname")
        ul = request.POST.get("lname")    
        u.email = ue
        u.first_name = uf
        u.last_name = ul
        u.save()

    return render(request,"acc/update.html")