from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AddProfileInfo(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name',
                  'email', 'bio', 'birth_date')
