from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Post, Comment, Image
from account.models import SocialUser
from django.contrib.auth.decorators import login_required
from .forms import CreatePostForm, ImageForm
from django.forms import modelformset_factory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

@login_required
def home(request):
    user = get_object_or_404(SocialUser, id=request.user.id)
    following_user = user.following.all()
    posts = Post.objects.exclude(author_id=request.user.id).filter(author__in=following_user, is_published=True)
    for post in posts:
        post.this_comments = Comment.objects.filter(post=post, parent=None, is_published=True).prefetch_related(
            'sub_comments').order_by('-created')

    return render(request, 'post/home.html', {'posts': posts})


@login_required
def explore(request):
    # users = SocialUser.objects.exclude(id=request.user.id).filter(is_active=True)
    users = SocialUser.objects.exclude(id=request.user.id).exclude(
        followers__id=request.user.id
    ).annotate(
        mutual_followers=Count('followers', filter=Q(followers__in=request.user.following.all()))
    ).order_by('-mutual_followers')[:10]
    posts = Post.objects.filter(is_published=True).annotate(
        interaction_count=Count('comments') + Count('save_by') + Count('likes')).order_by('-interaction_count')

    recent_posts = posts.filter(created_at__gte=timezone.now() - timedelta(days=1))
    final_posts = posts | recent_posts
    paginator = Paginator(final_posts, 12)
    page_number = request.GET.get(key='page', default=1)
    try:
        final_posts = paginator.page(page_number)
    except PageNotAnInteger:
        final_posts = paginator.page(1)
    except EmptyPage:
        final_posts = []

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'post/post_list_ajax.html', {'posts': final_posts})
    context = {
        "users": users,
        'posts': final_posts
    }
    return render(request, 'post/explore.html', context)


@login_required
def user_page(request, username):
    user = get_object_or_404(SocialUser, username=username, is_active=True)
    if request.user == user:
        return redirect('account:profile')
    return render(request, 'user/user_page.html', {'user': user})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post_id=post.id, parent=None, is_published=True).prefetch_related(
        'sub_comments').order_by('-created')
    return render(request, 'post/post_detail.html', {'post': post, 'comments': comments})


@login_required
def create_post(request):
    ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=1, max_num=10)

    if request.method == 'POST':
        post_form = CreatePostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())

        if post_form.is_valid() and formset.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            post_form.save_m2m()
            for form in formset.cleaned_data:
                if form:
                    image = form['file']
                    Image.objects.create(post=post, file=image)
            return redirect('account:profile')
    else:
        post_form = CreatePostForm()
        formset = ImageFormSet(queryset=Image.objects.none())

    return render(request, 'post/create_post.html', {'post_form': post_form, 'formset': formset})
