from django import forms
from .models import SocialUser


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
