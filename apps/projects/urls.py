from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list_view, name='list'),
    path('gantt/', views.project_gantt_view, name='gantt'),
    path('create/', views.project_create_view, name='create'),
    path('<uuid:pk>/', views.project_detail_view, name='detail'),
    path('<uuid:pk>/edit/', views.project_update_view, name='edit'),
    path('<uuid:project_pk>/add-milestone/', views.project_add_milestone_view, name='add_milestone'),
]
