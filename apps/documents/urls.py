from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.document_list_view, name='document_list'),
    path('blueprints/', views.blueprint_list_view, name='blueprint_list'),
    path('categories/', views.category_list_view, name='category_list'),
    path('upload/', views.document_create_view, name='document_create'),
    path('<uuid:pk>/', views.document_detail_view, name='document_detail'),
    path('<uuid:pk>/edit/', views.document_update_view, name='document_edit'),
    path('<uuid:pk>/add-version/', views.document_version_create_view, name='document_add_version'),
]
