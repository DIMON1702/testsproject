from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from .forms import SignUpForm, AddProfileInfo
from .models import User


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            #setattr(user.avatar,url,"/media/avatars/default-avatar.png")
            #user.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def save_profile(request):
    if request.method == "POST":
      #Get the posted form
        form = AddProfileInfo(request.POST, request.FILES)
        if form.is_valid():
            user_form = form.save(commit=False)
            new_user=request.user
            for field in form.Meta.fields:
                setattr(new_user,field, getattr(user_form, field))
            new_user.save()
    else:
        dictionary = {}
        form_user = AddProfileInfo()
        for field in form_user.Meta.fields:
            dictionary[field] = getattr(request.user, field)
        form = AddProfileInfo(initial=dictionary)
        
    return render(request, 'my_account.html', {'form': form})