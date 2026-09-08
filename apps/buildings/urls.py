from django.urls import path
from . import views

app_name = 'buildings'

urlpatterns = [
    path('', views.building_list_view, name='list'),
    path('create/', views.building_create_view, name='create'),
    path('<uuid:pk>/', views.building_detail_view, name='detail'),
    path('<uuid:pk>/edit/', views.building_update_view, name='edit'),
    path('<uuid:building_pk>/add-floor/', views.building_floor_create_view, name='add_floor'),
]
