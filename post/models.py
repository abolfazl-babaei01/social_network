from django.core.validators import FileExtensionValidator
from django.db import models
from account.models import SocialUser
from taggit.managers import TaggableManager
from django.utils import timezone
from datetime import timedelta


# Create your models here.


class Post(models.Model):
    """
    Model for user-generated posts with support for likes, tags, saves, and publication status.
    """

    author = models.ForeignKey(SocialUser, on_delete=models.CASCADE, related_name='posts')
    description = models.TextField()
    tags = TaggableManager()
    likes = models.ManyToManyField(SocialUser,blank=True, related_name='likes')
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
    """
    Model for storing images related to posts with file type validation.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images') # user post
    file = models.ImageField(upload_to='images/posts/', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """
    Model for managing comments on posts, supporting nested replies.
    """
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

class Story(models.Model):
    """
    Model for managing user stories, supporting both images and videos.
    """
    user = models.ForeignKey(SocialUser, on_delete=models.CASCADE, related_name='stories')
    file = models.FileField(upload_to='stories/', validators=[FileExtensionValidator(['mp4','webm', 'png', 'jpg', 'jpeg'])])
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_video(self):
        """
        Checks if the uploaded file is a video.
        """
        video_extensions = ['.mp4', '.webm']
        return any(self.file.url.endswith(ext) for ext in video_extensions)

    def is_image(self):
        """
        Checks if the uploaded file is an image.
        """
        image_extensions = ['.jpg', '.jpeg', '.png']
        return any(self.file.url.endswith(ext) for ext in image_extensions)

    def __str__(self):
        return f"Story by {self.user} - {self.created_at}"

class StoryVisit(models.Model):
    """
    Model for tracking user visits to stories, including user and IP address.
    """

    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='visits')
    user = models.ForeignKey(SocialUser, on_delete=models.CASCADE, related_name='story_visits')
    ip = models.GenericIPAddressField(protocol='both')

    def __str__(self):
        return f"{self.user} - {self.ip}"