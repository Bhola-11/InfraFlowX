from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('', views.maintenance_list_view, name='list'),
    path('create/', views.maintenance_create_view, name='create'),
    path('<uuid:pk>/', views.maintenance_detail_view, name='detail'),
    path('<uuid:pk>/edit/', views.maintenance_update_view, name='edit'),
    path('<uuid:pk>/complete/', views.maintenance_complete_view, name='complete'),
    path('<uuid:plan_pk>/add-action-log/', views.maintenance_action_log_add_view, name='add_action_log'),
]
