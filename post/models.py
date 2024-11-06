from django.core.validators import FileExtensionValidator
from django.db import models
from account.models import SocialUser
from taggit.managers import TaggableManager


# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(SocialUser, on_delete=models.CASCADE, related_name='posts')
    description = models.TextField()
    tags = TaggableManager()
    likes = models.ManyToManyField(SocialUser, blank=True, related_name='likes')
    total_likes = models.PositiveIntegerField(default=0)
    save_by = models.ManyToManyField(SocialUser, blank=True, related_name='saves')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"post by {self.author} - {self.id}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    file = models.ImageField(upload_to='images/posts/', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(SocialUser, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_comments', null=True, blank=True)
    text = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment by {self.author} - {self.post}"

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
