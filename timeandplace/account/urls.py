from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    # path('', views.home, name='home'),
    # path("register", views.register_request, name="register"),
    # path("login", views.login_request, name="login"),
    # path("logout", views.logout_request, name= "logout"),
]