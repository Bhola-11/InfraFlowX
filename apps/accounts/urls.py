from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/<uuid:pk>/', views.profile_view, name='profile_detail'),
    path('settings/', views.profile_settings_view, name='settings'),
    path('password-change/', views.password_change_view, name='password_change'),
    
    # User Management for Admins
    path('users/', views.user_list_view, name='user_list'),
    path('users/create/', views.user_create_view, name='user_create'),
    path('users/<uuid:pk>/edit/', views.user_edit_view, name='user_edit'),
    path('users/<uuid:pk>/toggle-status/', views.user_toggle_status_view, name='user_toggle_status'),
]
