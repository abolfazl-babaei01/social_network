# Django
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
# other
from .models import SocialUser
from .forms import CreateSocialUserForm, EditSocialUserForm


# Create your views here.


def index(request):
    return render(request, 'account/index.html')


def register(request):
    if request.method == 'POST':
        form = CreateSocialUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            form.save()
            login(request, user)
            return redirect('account:profile')

    else:
        form = CreateSocialUserForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    user = get_object_or_404(SocialUser, id=request.user.id)
    return render(request, 'account/profile.html', {'user': user})


@login_required
def setting(request):
    user = get_object_or_404(SocialUser, id=request.user.id)
    return render(request, 'account/setting.html', {'user': user})


@login_required
def edit_profile(request):
    user = get_object_or_404(SocialUser, id=request.user.id)
    if request.method == 'POST':
        form = EditSocialUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account:profile')
    else:
        form = EditSocialUserForm(instance=user)
    return render(request, 'account/edit_profile.html', {'user': user, 'form': form})