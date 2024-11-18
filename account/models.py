from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class SocialUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=11, unique=True)
    avatar = models.ImageField(upload_to='images/avatars/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    job = models.CharField(max_length=255, blank=True, null=True)
    following = models.ManyToManyField('self', through='Contact', related_name='followers', symmetrical=False)

    def __str__(self):
        return str(self.username)

    def get_followers(self):
        return [contact.user_from for contact in self.rel_to_set.all().order_by('-created')]

    def get_followings(self):
        return [contact.user_to for contact in self.rel_form_set.all().order_by('-created')]


class Contact(models.Model):
    user_from = models.ForeignKey(SocialUser, on_delete=models.CASCADE, related_name='rel_form_set')
    user_to = models.ForeignKey(SocialUser, on_delete=models.CASCADE, related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'

