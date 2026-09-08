from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('', views.maintenance_list_view, name='list'),
    path('', views.maintenance_list_view, name='plan_list'),
    path('create/', views.maintenance_create_view, name='create'),
    path('create/', views.maintenance_create_view, name='plan_create'),
    path('<uuid:pk>/', views.maintenance_detail_view, name='detail'),
    path('<uuid:pk>/', views.maintenance_detail_view, name='plan_detail'),
    path('<uuid:pk>/edit/', views.maintenance_update_view, name='edit'),
    path('<uuid:pk>/edit/', views.maintenance_update_view, name='plan_edit'),
    path('<uuid:pk>/complete/', views.maintenance_complete_view, name='complete'),
    path('<uuid:plan_pk>/add-action-log/', views.maintenance_action_log_add_view, name='add_action_log'),
    path('<uuid:plan_pk>/add-action-log/', views.maintenance_action_log_add_view, name='action_create'),
    path('actions/', views.maintenance_list_view, name='action_list'),
    path('actions/<uuid:pk>/edit/', views.maintenance_update_view, name='action_edit'),
]
