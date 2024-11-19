from django import forms
from .models import SocialUser
from django.contrib.auth.forms import AuthenticationForm

class CreateSocialUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = SocialUser
        fields = ['username', 'phone', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if SocialUser.objects.exclude(id=self.instance.id).filter(email__exact=email).exists():
            raise forms.ValidationError('This email already exists')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if SocialUser.objects.exclude(id=self.instance.id).filter(phone=phone).exists():
            raise forms.ValidationError('This phone already exists')
        return phone


class EditSocialUserForm(forms.ModelForm):
    class Meta:
        model = SocialUser
        fields = ['avatar', 'username', 'first_name', 'last_name', 'bio', 'job', 'email', 'phone']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if SocialUser.objects.exclude(id=self.instance.id).filter(email__exact=email).exists():
            raise forms.ValidationError('This email already exists')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if SocialUser.objects.exclude(id=self.instance.id).filter(phone=phone).exists():
            raise forms.ValidationError('This phone already exists')
        return phone


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=250, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'username or phone number'}))
    password = forms.CharField(max_length=250, required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'password'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = SocialUser.objects.filter(username=username, is_active=True, is_deleted=False)
        if not user:
            raise forms.ValidationError('Please enter a correct username and password. Note that both fields may be case-sensitive.')
        return username
