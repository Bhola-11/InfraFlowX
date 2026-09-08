from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.employee_list_view, name='list'),
    path('create/', views.employee_create_view, name='create'),
    path('<uuid:pk>/', views.employee_detail_view, name='detail'),
    path('<uuid:pk>/edit/', views.employee_update_view, name='edit'),
    path('<uuid:employee_pk>/add-skill/', views.add_employee_skill_view, name='add_skill'),
    path('<uuid:employee_pk>/add-certification/', views.add_employee_certification_view, name='add_certification'),
    
    # Skills & Matrix
    path('skills/', views.skill_matrix_view, name='skill_matrix'),
    path('skills/create/', views.skill_create_view, name='skill_create'),
    
    # Designations
    path('designations/', views.designation_list_view, name='designation_list'),
    path('designations/create/', views.designation_create_view, name='designation_create'),
    
    # Certifications
    path('certifications/', views.certification_list_view, name='certification_list'),
    path('certifications/create/', views.certification_create_view, name='certification_create'),
]
