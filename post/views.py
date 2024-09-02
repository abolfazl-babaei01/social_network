from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from account.models import SocialUser
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def home(request):
    user = get_object_or_404(SocialUser, id=request.user.id)
    following_user = user.following.all()
    posts = Post.objects.exclude(author_id=request.user.id).filter(author__in=following_user, is_published=True)
    return render(request, 'post/home.html', {'posts': posts})


def explore(request):
    users = SocialUser.objects.exclude(id=request.user.id).filter(is_active=True)
    pop_posts = Post.objects.filter(total_likes__gte=1).order_by('-total_likes')
    context = {
        "users": users,
        'pop_posts': pop_posts
    }
    return render(request, 'post/explore.html', context)


def user_page(request, username):
    user = get_object_or_404(SocialUser, username=username, is_active=True)
    if request.user == user:
        return redirect('account:profile')
    return render(request, 'user/user_page.html', {'user': user})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post_id=post.id, parent=None, is_published=True).prefetch_related(
        'sub_comments').order_by('-created')
    return render(request, 'post/post_detail.html', {'post': post, 'comments': comments})
