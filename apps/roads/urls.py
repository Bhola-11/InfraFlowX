from django.urls import path
from . import views

app_name = 'roads'

urlpatterns = [
    path('', views.road_list_view, name='list'),
    path('create/', views.road_create_view, name='create'),
    path('<uuid:pk>/', views.road_detail_view, name='detail'),
    path('<uuid:pk>/edit/', views.road_update_view, name='edit'),
    
    # Defects
    path('defects/', views.road_defect_list_view, name='defect_list'),
    path('defects/create/', views.road_defect_create_view, name='defect_create'),
    path('defects/<int:pk>/resolve/', views.road_defect_resolve_view, name='defect_resolve'),
]
