from django import forms
from .models import Post, Image, Story
from django.forms import modelformset_factory
from django.core.validators import ValidationError

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'tags']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['file']


def validate_file_extension(value):
    if not value.name.endswith(('.mp4', '.png', '.jpg', '.jpeg')):
        raise ValidationError("Only files with extensions .mp4, .png, .jpg, or .jpeg are allowed.")


class CreateStoryForm(forms.ModelForm):
    file = forms.FileField(validators=[validate_file_extension])
    class Meta:
        model = Story
        fields = ['file']
