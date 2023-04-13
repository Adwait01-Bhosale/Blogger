from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Account

# Create your views here.

def login_user(request):
    print("Inside Login")
    # if request.user.is_authenticated:
    #     print("First If")
    #     return redirect('home')
    if request.method == 'POST':
        print("POST Request!!")
        data = request.POST
        email = data['login_email']
        password = data['login_pass']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            print("Authenticated")
            login(request, user)
            return redirect('home')
        else:
            print("Not Authenticated!!")
            messages.error(request, "Couldn't Login. Please check your credentials.")
    return render(request, 'userauth/login.html')

def signup(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    if request.method == 'POST':
        data = request.POST
        fullname = data['signup_fullname']
        email = data['signup_email']
        user_image=request.FILES.get('user_image')
        print(f"User Image is: {user_image}")
        domain=data['domain']
        password = data['signup_pass']
        password2 = data['signup_pass2']
        if password == password2:
            if Account.objects.filter(email=email).exists():
                messages.info(request, 'Email already in use. Please use another email!')
                return redirect('signup')
            if Account.objects.filter(fullname=fullname).exists():
                messages.info(request, 'Username already in use. Please use another username!')
                return redirect('signup')
            else:
                user=Account.objects.create_user(fullname=fullname, email=email, domain=domain, password=password)
                user.save()
                login(request, user)
                messages.info(request, 'Account created successfully.')
                return redirect('login')
        else:
            messages.error(request, 'Please make sure the passwords match.')
            return redirect('signup')
    return render(request, 'userauth/signup.html')

def logout_user(request):
    logout(request)
    messages.success(request, "Logged out Successfully!!")
    return redirect('home')