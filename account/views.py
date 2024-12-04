# Django
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.templatetags.static import static

# other
from .models import SocialUser, Contact
from .forms import EditSocialUserModelForm, RegisterModelForm
from post.models import Post, Comment
from pprint import pprint


# Create your views here.


def register(request):
    """
    Handles the registration of a new social user.

    This view renders a registration form and processes the submitted data to
    create a new user. If the registration is successful, the user is logged in
    and redirected to their profile.

    Args:
        request (Http): User http request for render registration form.

    Returns:
        HttpResponse:  Renders the registration form page if the request is
        GET or the form is invalid. Redirects to the profile page if the
        registration is successful.
    """

    if request.method == 'POST':
        form = RegisterModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(form.cleaned_data['password1'])
            form.save()
            login(request, user)
            return redirect('account:profile')

    else:
        form = RegisterModelForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    """
    Handles the profile page for current user.

    Args:
        request (Http): User http request for render profile page.

    Returns:
        HttpResponse:  Renders the profile page if the user is logged.

    """
    user = SocialUser.objects.filter(id=request.user.id, is_active=True, is_deleted=False).first()
    has_active_story = user.stories.filter(is_delete=False).exists()
    context = {
        'user': user,
        'has_active_story': has_active_story
    }
    return render(request, 'account/profile.html', context)


@login_required
def setting(request):
    """
    Handles the settings page for current user.
    This view renders the settings page for the current user.
    """
    user = SocialUser.objects.filter(id=request.user.id, is_active=True, is_deleted=False).first()
    return render(request, 'account/setting.html', {'user': user})


@login_required
def edit_profile(request):
    """
    Handles the profile editing functionality for the current user.

    This view allows authenticated users to edit their profile information,
    such as updating their personal details or uploading a new profile picture.
    The changes are saved if the submitted form is valid.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
        about the request.

    Returns:
        HttpResponse:
            - Renders the edit profile page with the current user's information
              and an empty or pre-filled form (if the request is GET).
            - Redirects to the profile page if the form submission is successful.
    """


    user = SocialUser.objects.filter(id=request.user.id, is_active=True, is_deleted=False).first()
    if request.method == 'POST':
        form = EditSocialUserModelForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account:profile')
    else:
        form = EditSocialUserModelForm(instance=user)
    return render(request, 'account/edit_profile.html', {'user': user, 'form': form})


@require_POST
def follow_user(request):
    """
    Handles the follow/unfollow functionality for users.

    This view allows the current user to follow or unfollow another user.
    If the targeted user is already followed, the function will remove the
    follow relationship (unfollow). Otherwise, it creates a new follow
    relationship.

    Args:
        request (HttpRequest): The HTTP request object containing a POST
        parameter `user_id` that specifies the ID of the user to follow or unfollow.

    Returns:
        JsonResponse:
            - If the follow/unfollow operation is successful, returns a JSON response
              containing:
                - `followers_count`: The updated number of followers of the targeted user.
                - `following_count`: The updated number of users the current user is following.
                - `followed`: A boolean indicating whether the current user is now following
                  the targeted user.
            - If the user ID is invalid or the user is not found, returns a JSON response
              with an appropriate error message.
            - If the current user attempts to follow themselves, returns a JSON response
              with `follow_yourself: True`.

    """

    user_id = request.POST.get('user_id')
    if user_id:
        try:
            user = get_object_or_404(SocialUser, id=user_id, is_active=True, is_deleted=False)
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
            print(e)
            return JsonResponse({'error': 'Post not found'})
    return JsonResponse({'Bad request': 'Post not found'})


@require_POST
def add_comment(request):
    post_id = request.POST.get('post_id')
    parent_id = request.POST.get('parent_id')
    comment_text = request.POST.get('comment_text')
    if comment_text:
        try:
            new_comment = Comment(post_id=post_id, author_id=request.user.id, parent_id=parent_id, text=comment_text)
            new_comment.save()
            comments = (Comment.objects.filter(is_published=True, post_id=post_id, parent=None)
                        .prefetch_related('sub_comments')).order_by('-created')
            comments_count = comments.count()
            context = {'comments_count': comments_count, 'comments': comments}
            rendered_html = render_to_string('partials/post_comment_partial.html', context, request=request)
            return JsonResponse({'html': rendered_html})
        except Exception as e:
            print(e)
    else:
        return JsonResponse({'error': 'Comment text required'})
    return JsonResponse({'error': 'Post not found'})


def user_contact(request, username, relation):
    user = get_object_or_404(SocialUser, username=username, is_active=True, is_deleted=False)
    if relation == 'followers':
        users = user.get_followers()
    elif relation == 'following':
        users = user.get_followings()
    else:
        raise Http404('Invalid relation')
    context = {'users': users, 'relation': relation, 'user': user}
    return render(request, 'account/user_contact.html', context)


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, is_published=True)
    if post.author == request.user:
        post.delete()
        return redirect('account:profile')


def liked_posts(request):
    user = SocialUser.objects.filter(id=request.user.id, is_active=True, is_deleted=False).first()
    context = {'user': user}
    return render(request, 'account/liked_posts.html', context)


def saved_posts(request):
    user = SocialUser.objects.filter(id=request.user.id, is_active=True, is_deleted=False).first()
    context = {'user': user}
    return render(request, 'account/saved_posts.html', context)


def question_delete_account(request):
    return render(request, 'account/delete_account.html', {})


def deleted_account(request):
    if request.method == 'POST':
        user = SocialUser.objects.filter(id=request.user.id, is_active=True, is_deleted=False).first()
        if not user:
            messages.error(request, 'this user alerdy is deleted')
        user.is_deleted = True
        user.username += '_deleted_' + str(user.id)
        user.reason_deleting_account = request.POST.get('reason')
        user.save()
        logout(request)
        return redirect('account:login')
    else:
        pass
