from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from .forms import SignUpForm, AddProfileInfo
#from .forms import AddProfileInfo
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
    #form = AddProfileInfo()
    if request.method == "POST":
      # Get the posted form
        form = AddProfileInfo(request.POST, request.FILES)
        if form.is_valid():
            user_form = form.save(commit=False)
            new_user = request.user
            for field in form.Meta.fields:
                setattr(new_user, field, getattr(user_form, field))
            new_user.save()
    else:
        dictionary = {}
        for field in AddProfileInfo().Meta.fields:
            dictionary[field] = getattr(request.user, field)
        form = AddProfileInfo(initial=dictionary)

    # BUG - если не загружается новое изображение и сохраняются изменения - выскакивает ошибка
    return render(request, 'my_account.html', {'form': form})
