from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True,)
    avatar = models.ImageField(
        'profile picture', upload_to='avatars', null=True, blank=True)
