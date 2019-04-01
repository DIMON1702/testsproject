from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect

from .forms import SignUpForm, AddProfileInfo
from .models import User


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def save_profile(request):
    if request.method == "POST":
        form = AddProfileInfo(request.POST, request.FILES)
        if form.is_valid():
            user_form = form.save(commit=False)
            new_user = request.user
            for field in form.Meta.fields:
                setattr(new_user, field, getattr(user_form, field))
            new_user.save()
    else:
        dictionary = {}
        form_user = AddProfileInfo()
        for field in form_user.Meta.fields:
            dictionary[field] = getattr(request.user, field)
        form = AddProfileInfo(initial=dictionary)
    return render(request, 'my_account.html', {'form': form})
