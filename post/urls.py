from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.home, name='index'),
    path('explore/', views.explore, name='explore'),
    path('explore/user/<str:username>', views.user_page, name='user_page'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
]
