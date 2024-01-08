from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from coder.models import *
from coder.forms import *
from coder.emailbackend import EmailBackEnd
from django.contrib.auth.decorators import login_required
from coder.decorators import unauthenticated_user
from django.contrib.auth import authenticate, login, logout


@unauthenticated_user
def Register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # check email
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already exists!')
            return redirect('register')

        # check username
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username is already exists!')
            return redirect('register')

        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        messages.success(
            request, 'You are registered successfully. Now Login!')
        return redirect('login')

    return render(request, 'registration/signup.html')


@unauthenticated_user
def Login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = EmailBackEnd.authenticate(
            request, username=email, password=password)

        if user != None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email and Password are invalid !')
            return redirect('login')

    return render(request, 'registration/login.html')


@login_required(login_url='login')
def profile(request):
    return render(request, 'user/profile_page.html')


@login_required(login_url='login')
def profile_update(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES,
                           instance=request.user.profile)
        if form.is_valid():
            form.save()
            username = request.user.username
            messages.success(
                request, f'{username}, Your Profile is successfully updated.')
            return render(request, 'user/profile_page.html')
    else:
        form = ProfileForm(instance=request.user.profile)
    context = {
        'form': form,
    }
    return render(request, 'user/profile.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')
