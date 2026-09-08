from django.urls import path
from . import views

app_name = 'inspections'

urlpatterns = [
    path('', views.inspection_list_view, name='list'),
    path('', views.inspection_list_view, name='inspection_list'),
    path('create/', views.inspection_create_view, name='create'),
    path('create/', views.inspection_create_view, name='inspection_create'),
    path('<uuid:pk>/', views.inspection_detail_view, name='detail'),
    path('<uuid:pk>/', views.inspection_detail_view, name='inspection_detail'),
    path('<uuid:pk>/edit/', views.inspection_update_view, name='edit'),
    path('<uuid:pk>/edit/', views.inspection_update_view, name='inspection_edit'),
    path('<uuid:pk>/approve/', views.inspection_approve_view, name='approve'),
    path('<uuid:inspection_pk>/add-checklist/', views.inspection_add_checklist_view, name='add_checklist'),
]

