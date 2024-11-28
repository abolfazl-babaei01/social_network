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
    is_deleted = models.BooleanField(default=False)
    reason_deleting_account = models.TextField(blank=True, null=True, default='')


    def __str__(self):
        return str(self.username)

    def get_followers(self):
        return [contact.user_from for contact in self.rel_to_set.filter(user_from__is_active=True, user_from__is_deleted=False).order_by('-created')]

    def get_followings(self):
        # normal loop
        # for contact in self.rel_form_set.all():
        #     return contact.user_to

        return [contact.user_to for contact in self.rel_from_set.filter(user_to__is_active=True, user_to__is_deleted=False).order_by('-created')]



class Contact(models.Model):
    """
    Through Model :

    user = SocialUser.objects.get(pk=1) اینجا یک کاربر رو بصورت فرضی از دیتابیس میگیریم

    user_followings = user.rel_from_set.all() اینجا با استفاده از اون نام ارتباطی فالووینگ ها یا همون کسایی که فالو کرده رو میگیریم

    user_followers = user.rel_to_set.all()  اینجا با استفاده از اون نام ارتباطی همه اون فالوور ها یا همون کسایی که فالوش کردن رو میگیریم

    """
    # شخصی که فالو شده است
    user_from = models.ForeignKey(SocialUser, on_delete=models.CASCADE, related_name='rel_from_set')
    # شخصی که فالو کرده اسن
    user_to = models.ForeignKey(SocialUser, on_delete=models.CASCADE, related_name='rel_to_set')
    # تاریخ ایجاد ارتباط با همان آبجکت
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'
