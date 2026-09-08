from django.urls import path
from . import views

app_name = 'locations'

urlpatterns = [
    path('', views.location_list_view, name='list'),
    path('', views.location_list_view, name='location_list'),
    path('map/', views.gis_map_view, name='map'),
    path('map/', views.gis_map_view, name='gis_map'),
    path('api/geojson/', views.geojson_api_view, name='geojson_api'),
    path('create/', views.location_create_view, name='create'),
    path('create/', views.location_create_view, name='location_create'),
    path('<uuid:pk>/', views.location_detail_view, name='detail'),
    path('<uuid:pk>/', views.location_detail_view, name='location_detail'),
    path('<uuid:pk>/edit/', views.location_update_view, name='edit'),
    path('<uuid:pk>/edit/', views.location_update_view, name='location_edit'),
]
