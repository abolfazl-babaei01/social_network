from django.http import HttpResponse
from django.shortcuts import render
from .forms import CreateSocialUserForm


# Create your views here.


def register(request):
    if request.method == 'POST':
        form = CreateSocialUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponse('User created successfully!')

    else:
        form = CreateSocialUserForm()
    return render(request, 'account/register.html', {'form': form})
