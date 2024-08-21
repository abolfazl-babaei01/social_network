# Django
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.views.decorators.http import require_POST
from django.http import JsonResponse

# other
from .models import SocialUser, Contact
from .forms import CreateSocialUserForm, EditSocialUserForm
from post.models import Post


# Create your views here.


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


@require_POST
def follow_user(request):
    user_id = request.POST.get('user_id')

    if user_id:
        try:
            user = get_object_or_404(SocialUser, id=user_id, is_active=True)
            if user == request.user:
                return JsonResponse({'follow_yourself': True})
            if request.user in user.followers.all():
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
                followed = False
            else:
                Contact.objects.create(user_from=request.user, user_to=user)
                followed = True
            followers_count = user.followers.count()
            following_count = user.following.count()
            return JsonResponse({'followers_count': followers_count, 'following_count': following_count,
                                 'followed': followed})

        except SocialUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'})
    return JsonResponse({'error': 'Bad request'})


@require_POST
def like_post(request):
    post_id = request.POST.get('post_id')
    if post_id:
        try:
            post = get_object_or_404(Post, id=post_id, is_published=True)
            if request.user in post.likes.all():
                post.likes.remove(request.user)
                liked = False
            else:
                post.likes.add(request.user)
                liked = True
            response = {'liked': liked, 'like_count': post.likes.count()}
            return JsonResponse(response)
        except Exception as e:
            return JsonResponse({'error': e})
    return JsonResponse({'Bad request': 'Post not found'})


@require_POST
def save_post(request):
    post_id = request.POST.get('post_id')
    if post_id:
        try:
            post = get_object_or_404(Post, id=post_id, is_published=True)
            if request.user in post.save_by.all():
                post.save_by.remove(request.user)
                saved = False
            else:
                post.save_by.add(request.user)
                saved = True
            return JsonResponse({'saved': saved})
        except Exception as e:
            return JsonResponse({'error': 'Post not found'})
    return JsonResponse({'Bad request': 'Post not found'})
