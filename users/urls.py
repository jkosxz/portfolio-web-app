from django.urls import path
from . import views

urlpatterns = [
    path('login_user', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('register', views.register_redirect, name='register_redirect'),
    path('login', views.login_redirect, name='login_redirect')
]