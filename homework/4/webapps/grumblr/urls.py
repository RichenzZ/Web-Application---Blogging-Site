"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
import grumblr.views

urlpatterns = [
    path('', grumblr.views.home),
    path('logout', auth_views.logout_then_login, name='logout'), #default redirect to settings.LOGIN_URL 
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'), 
    path('signup', grumblr.views.sign_up, name='signup'),
    path('add_post', grumblr.views.add_post, name='add_post'),
    path('photo/<int:user_id>', grumblr.views.get_photo, name='photo'),
    path('follow/<int:user_id>', grumblr.views.follow, name='follow'),
    path('unfollow/<int:user_id>', grumblr.views.unfollow, name='unfollow'),
    path('view_profile/<int:user_id>', grumblr.views.view_profile, name='view_profile'),
    path('edit_profile/', grumblr.views.add_entry, name='edit_profile'),
    path('profile', grumblr.views.profile, name='profile'),
    path('global', grumblr.views.home, name='home'),
    path('follower_stream', grumblr.views.follower_stream, name='follower_stream'),
    re_path(r'^email_confirm/(?P<username>\w+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    grumblr.views.email_confirm, name='email_confirm'),
    path('reset_password/', grumblr.views.reset_password, name='reset_password'),
    path('password_change/', grumblr.views.password_change, name='password_change'),
    path('forget_password/', grumblr.views.forget_password, name='forget_password'),
    re_path(r'^password_confirm/(?P<username>\w+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    grumblr.views.password_confirm, name='password_confirm'),

]

