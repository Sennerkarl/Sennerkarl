from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST': # if is the method used by online user (HTTP) - as defined in template
        form = UserRegisterForm(request.POST) #POST matches the Form method in the template
        if form.is_valid():
            form.save() #saves form as a new User
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in')
            return redirect('login') #name of url
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form}) # even if form invalid still keeps what was input

@login_required #strong decorater to only allow 
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user) #set new data, fill the form with data from user
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile) #aslo grabbing the images

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account has been updated')
            return redirect('profile') # post get redirect pattern comes into play (are you sure you want to reload?)

    else:
        u_form = UserUpdateForm(instance=request.user) #fill the form with data from user
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = { # make dictionary which then renderable and then accessible in template
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)