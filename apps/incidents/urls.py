from django.urls import path
from . import views

app_name = 'incidents'

urlpatterns = [
    path('', views.incident_list_view, name='incident_list'),
    path('', views.incident_list_view, name='list'),
    path('create/', views.incident_create_view, name='incident_create'),
    path('create/', views.incident_create_view, name='create'),
    path('<uuid:pk>/', views.incident_detail_view, name='incident_detail'),
    path('<uuid:pk>/', views.incident_detail_view, name='detail'),
    path('<uuid:pk>/edit/', views.incident_update_view, name='incident_edit'),
    path('<uuid:pk>/edit/', views.incident_update_view, name='edit'),
    path('<uuid:pk>/dispatch/', views.incident_dispatch_view, name='dispatch_create'),
    path('<uuid:incident_pk>/dispatch/', views.incident_dispatch_view, name='incident_dispatch'),
    path('<uuid:pk>/resolve/', views.incident_resolve_view, name='incident_resolve'),
]
