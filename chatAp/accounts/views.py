from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegistrationForm,UserLoginForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from chat.models import Thread
from .models import User, FriendRequest
from django.db.models import Q


# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    return render(request, 'dashboard/home.html')

def Register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data['username']
            # email = form.cleaned_data['email']
            # password = form.cleaned_data['password']
            # user = User.objects.create_user(username=username, email=email, password=password)
            # username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegistrationForm()


    return render(request, 'register.html', {'form': form})



def LoginPage(request):
    error_message = None
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {user.username}- have a good conversations!')
                return redirect('dashboard')
            else:
                error_message = 'Invalid username or password.'
    else:
        form = UserLoginForm()
    return render(request, 'login.html',  {'form': form})
@login_required
def profile(request):
    if request.method == 'POST':

        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            if u_form.has_changed() or p_form.has_changed():
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account has been updated!')
            else:
                messages.info(request, 'No changes were made.')

            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    friends_count = Thread.objects.filter(Q(first_person=request.user) | Q(second_person=request.user)).count()
    context = {
        'u_form':u_form,
        'p_form': p_form,
        'friends_count': friends_count,
               }
    return render(request, 'dashboard/profile.html',context=context)








def LogoutPage(request):
    logout(request)
    return redirect('login')