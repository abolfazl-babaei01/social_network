from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.home, name='index'),
    path('explore/', views.explore, name='explore'),
    path('explore/user/<str:username>', views.user_page, name='user_page'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),

    path('story-detail/<int:user_id>/', views.story_detail, name='story_detail'),
    path('add-visit-story/<int:story_id>/<int:user_id>/', views.add_visit_story, name='add_visit_story'),
    path('create-post/', views.create_post, name='create_post'),
    path('create-story/', views.create_story, name='create_story'),

    path('delete-story/<int:story_id>/', views.delete_story, name='delete_story'),

]
