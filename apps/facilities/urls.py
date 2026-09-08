from django.urls import path
from . import views

app_name = 'facilities'

urlpatterns = [
    path('', views.facility_list_view, name='list'),
    path('create/', views.facility_create_view, name='create'),
    path('<uuid:pk>/', views.facility_detail_view, name='detail'),
    path('<uuid:pk>/edit/', views.facility_update_view, name='edit'),
    path('<uuid:equipment_pk>/add-service-log/', views.service_log_create_view, name='add_service_log'),
]
