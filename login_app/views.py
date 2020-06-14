from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def form(request):
    return render(request, 'login.html')

def success(request): 
    return render(request, 'logged_in.html', {"user": User.objects.get(id=request.session['user_id'])})

def registered(request):

    errors = User.objects.basic_validator(request.POST)

    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")

    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)

        request.session['user_id'] = user.id

        messages.error(request, "Successfully registered!")

        return redirect("/success")

def logout(request):
    request.session.flush()
    return redirect('/')

def login(request):

    user = User.objects.filter(email=request.POST['email'])

    if len(user)>0:
        logged_user = user[0]

        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            messages.error(request, "Successfully logged in!")
            return redirect ("/success")
        
    else:
        messages.error(request, "Password and email do not match")
        return redirect("/")