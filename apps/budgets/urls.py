from django.urls import path
from . import views

app_name = 'budgets'

urlpatterns = [
    path('', views.budget_list_view, name='list'),
    path('', views.budget_list_view, name='budget_list'),
    path('create/', views.budget_create_view, name='create'),
    path('create/', views.budget_create_view, name='budget_create'),
    path('<uuid:pk>/', views.budget_detail_view, name='detail'),
    path('<uuid:pk>/', views.budget_detail_view, name='budget_detail'),
    path('<uuid:pk>/edit/', views.budget_update_view, name='edit'),
    path('<uuid:pk>/edit/', views.budget_update_view, name='budget_edit'),
    path('<uuid:budget_pk>/add-allocation/', views.budget_add_allocation_view, name='add_allocation'),
    path('<uuid:budget_pk>/add-allocation/', views.budget_add_allocation_view, name='allocation_create'),
]
