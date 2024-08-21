from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    # auth views
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # password change
    path('password-change/', auth_views.PasswordChangeView.as_view(success_url='done'), name="password_change"),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    # password rest
    path('password-reset/', auth_views.PasswordResetView.as_view(success_url='done'), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url='/account/password-reset-complete/'),
         name="password_reset_confirm"),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # profile
    path('profile/', views.profile, name='profile'),
    path('profile/setting/', views.setting, name='setting'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # user actions
    path('follow-user/', views.follow_user, name='follow_user'),
    path('like-post/', views.like_post, name='like_post'),
    path('save-post/', views.save_post, name='save_post'),
]
