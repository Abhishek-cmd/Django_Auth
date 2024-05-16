from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your views here.
# By default function call

def index(request):
   if request.user.is_anonymous:
       return redirect('login')
   return render(request, 'index.html')

# Login function call
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/')  # redirect to the home page or any other page
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


# Register function call   
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if not username or not password or not email:
            messages.error(request, 'All fields are required.')
            return render(request, 'login.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'login.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'login.html')

        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            messages.success(request, 'User created successfully')
            return redirect('login')
        except ValidationError as e:
            messages.error(request, f'Error creating user: {e.messages[0]}')
            return render(request, 'login.html')
        
    return redirect('login')

# Logout function call
def logoutuser(request):
    logout(request)
    return redirect('login')
