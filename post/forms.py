from django import forms
from .models import Post, Image
from django.forms import modelformset_factory


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'tags']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['file']