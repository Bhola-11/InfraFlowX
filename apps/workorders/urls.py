from django.urls import path
from . import views

app_name = 'workorders'

urlpatterns = [
    path('', views.workorder_list_view, name='list'),
    path('create/', views.workorder_create_view, name='create'),
    path('<uuid:pk>/', views.workorder_detail_view, name='detail'),
    path('<uuid:pk>/edit/', views.workorder_update_view, name='edit'),
    path('<uuid:pk>/status/<str:new_status>/', views.workorder_status_update_view, name='status_update'),
    path('<uuid:wo_pk>/add-task/', views.workorder_add_task_view, name='add_task'),
]
