from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name="login"),
    path('register/', views.register, name='register'),
    path('', include('django.contrib.auth.urls')),
    path('edit/', views.edit, name='edit'),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile_liked_me/<int:pk>/', views.profile_liked_me, name='profile_liked_me'),
    path('profile/<int:pk>/', views.profile, name="profile"),
    path('preferences/<int:pk>/', views.preferences, name="preferences"),
    path('edit_preferences/', views.edit_preferences, name='edit_preferences'),
    path('edit_timenplace/', views.edittimenplace, name='edit_timenplace'),
    path('filter_profile_list/', views.filter_profile_list, name='filter_profile_list'),
    path('ajax/load-locations/', views.load_locations, name='ajax_load_locations'), # AJAX
    path('match_feedback/', views.submitFeedback, name='submitFeedback'),

    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]