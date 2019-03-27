from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True,
                            widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AddProfileInfo(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name',
                  'email', 'bio', 'birth_date')
