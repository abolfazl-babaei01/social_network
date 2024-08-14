from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class SocialUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=11, unique=True)
    avatar = models.ImageField(upload_to='images/avatars/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    job = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.username)
