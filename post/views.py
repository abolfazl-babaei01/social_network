# query modules
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
# my db models
from .models import Post, Comment, Image, Story, StoryVisit
from account.models import SocialUser
# forms
from .forms import CreatePostForm, ImageForm, CreateStoryForm
from django.forms import modelformset_factory
# decorators and paginator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# http modules
from django.http import JsonResponse, HttpRequest
# my utils
from utils.client_info import get_client_ip
# times modules
from django.utils import timezone
from datetime import timedelta
from django.utils.timesince import timesince
from pprint import pprint


# Create your views here.

@login_required
def home(request):
    user = get_object_or_404(SocialUser, id=request.user.id, is_active=True, is_deleted=False)
    current_user_stories = user.stories.filter(is_delete=False)
    following_user = user.following.filter(is_active=True, is_deleted=False)
    stories = Story.objects.filter(user__in=following_user, is_delete=False).select_related('user')
    story_users = {story.user for story in stories}

    suggested_users = SocialUser.objects.exclude(id=request.user.id).exclude(followers__id=request.user.id).annotate(
        mutual_followers=Count('followers', filter=Q(followers__in=request.user.following.all()))).filter(
        is_active=True, is_deleted=False).order_by('-mutual_followers')[:5]

    posts = Post.objects.exclude(author_id=request.user.id).filter(author__in=following_user, is_published=True)
    for post in posts:
        post.this_comments = Comment.objects.filter(post=post, parent=None, is_published=True).prefetch_related(
            'sub_comments').order_by('-created')
    context = {
        'current_user_stories': current_user_stories,
        'stories': stories,
        'story_users': story_users,
        'posts': posts,
        'user': user,
        'suggested_users': suggested_users
    }
    return render(request, 'post/home.html', context)


@login_required
def explore(request):
    # get pop posts
    posts = Post.objects.filter(is_published=True).annotate(
        interaction_count=Count('comments') + Count('save_by') + Count('likes')).order_by('-interaction_count')

    recent_posts = posts.filter(created_at__gte=timezone.now() - timedelta(days=1))


    final_posts = posts | recent_posts
    # add pagination with ajax
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

    # add search form coding
    query = request.GET.get('q')
    result_search = []
    if query:
        result_search = SocialUser.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))

    context = {
        'posts': final_posts,
        'result_search': result_search
    }

    return render(request, 'post/explore.html', context)


@login_required
def user_page(request, username):
    user = get_object_or_404(SocialUser, username=username, is_active=True, is_deleted=False)
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


@login_required
def story_detail(request, user_id):
    stories = Story.objects.filter(user_id=user_id, is_delete=False).prefetch_related('visits')
    user = SocialUser.objects.get(id=user_id)
    context = {
        'stories': stories,
        'user': user,
    }
    return render(request, 'post/story_detail.html', context)


@login_required
def add_visit_story(request, story_id, user_id):
    user = SocialUser.objects.get(id=user_id, is_active=True, is_deleted=False)
    visit_count = StoryVisit.objects.exclude(user_id=request.user.id).filter(story_id=story_id).count()
    viewers = list(
        StoryVisit.objects.filter(story_id=story_id)
        .select_related('user')
        .values('user__id', 'user__username', 'user__avatar')
    )
    story_instance = Story.objects.get(id=story_id, is_delete=False)
    time_since_created = timesince(story_instance.created_at, timezone.now())
    data = {
        'viewers': viewers,
        'visit_count': visit_count,
        'time_since_created': time_since_created,
    }
    try:
        if not user == request.user:
            user_ip = get_client_ip(request)
            has_been_visited = StoryVisit.objects.filter(story_id=story_id, ip__iexact=user_ip).exists()
            if not has_been_visited:
                StoryVisit.objects.create(story_id=story_id, user_id=request.user.id, ip=user_ip)
    except Exception as e:
        print(f'error this view (add_visit_story): {e}')
    return JsonResponse(data)


@login_required
def create_story(request: HttpRequest):
    if request.method == 'POST':
        form = CreateStoryForm(request.POST, request.FILES)
        if form.is_valid():
            new_story = form.save(commit=False)
            new_story.user = request.user
            new_story.save()
            return redirect('post:index')

    else:
        form = CreateStoryForm()
    return render(request, 'post/create_story.html', {'form': form})


def delete_story(request, story_id):
    story = get_object_or_404(Story, id=story_id, is_delete=False)
    if request.user == story.user:
        story.is_delete = True
        story.save()
        return redirect('post:index')

