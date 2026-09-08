from django.urls import path
from . import views

app_name = 'organizations'

urlpatterns = [
    path('', views.organization_list_view, name='list'),
    path('create/', views.organization_create_view, name='create'),
    path('<uuid:pk>/', views.organization_detail_view, name='detail'),
    path('<uuid:pk>/edit/', views.organization_update_view, name='edit'),
    path('tree/', views.organization_hierarchy_tree_view, name='tree'),
    path('<uuid:pk>/tree/', views.organization_hierarchy_tree_view, name='tree_detail'),
    
    # Regions
    path('regions/', views.region_list_view, name='region_list'),
    path('regions/create/', views.region_create_view, name='region_create'),
    
    # Departments
    path('departments/', views.department_list_view, name='department_list'),
    path('departments/create/', views.department_create_view, name='department_create'),
    
    # Offices
    path('offices/', views.office_list_view, name='office_list'),
    path('offices/create/', views.office_create_view, name='office_create'),
    
    # Teams
    path('teams/', views.team_list_view, name='team_list'),
    path('teams/create/', views.team_create_view, name='team_create'),
]
