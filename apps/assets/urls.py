from django.urls import path
from . import views

app_name = 'assets'

urlpatterns = [
    path('', views.asset_list_view, name='list'),
    path('', views.asset_list_view, name='asset_list'),
    path('create/', views.asset_create_view, name='create'),
    path('create/', views.asset_create_view, name='asset_create'),
    path('<uuid:pk>/', views.asset_detail_view, name='detail'),
    path('<uuid:pk>/', views.asset_detail_view, name='asset_detail'),
    path('<uuid:pk>/edit/', views.asset_update_view, name='edit'),
    path('<uuid:pk>/edit/', views.asset_update_view, name='asset_edit'),
    path('<uuid:pk>/status-change/', views.asset_status_change_view, name='status_change'),
    path('categories/', views.asset_category_list_view, name='category_list'),
    path('categories/create/', views.asset_category_create_view, name='category_create'),
]

