from django import forms
from .models import SocialUser


class CreateSocialUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = SocialUser
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if SocialUser.objects.exclude(id=self.instance.id).filter(email__exact=email).exists():
            raise forms.ValidationError('This email already exists')
        return email
