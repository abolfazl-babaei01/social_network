from django import forms
from .models import SocialUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CreateSocialUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
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



class EditSocialUserForm(UserChangeForm):
    class Meta(UserCreationForm.Meta):
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
    username = forms.CharField(max_length=250, required=True)
    password = forms.CharField(max_length=250, required=True)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = SocialUser.objects.filter(username=username, is_active=True, is_deleted=False)
        if not user:
            raise forms.ValidationError(
                'Please enter a correct username and password. Note that both fields may be case-sensitive.')
        return username

class RegisterModelForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password(again)'}))
    class Meta:
        model = SocialUser
        fields = ['username', 'phone', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2