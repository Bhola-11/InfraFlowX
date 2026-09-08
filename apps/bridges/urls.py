from django.urls import path
from . import views

app_name = 'bridges'

urlpatterns = [
    path('', views.bridge_list_view, name='list'),
    path('create/', views.bridge_create_view, name='create'),
    path('<uuid:pk>/', views.bridge_detail_view, name='detail'),
    path('<uuid:pk>/edit/', views.bridge_update_view, name='edit'),
    path('<uuid:bridge_pk>/add-component/', views.bridge_component_add_view, name='add_component'),
]
