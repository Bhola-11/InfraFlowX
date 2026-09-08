from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.expense_list_view, name='list'),
    path('create/', views.expense_create_view, name='create'),
    path('<uuid:pk>/', views.expense_detail_view, name='detail'),
    path('<uuid:pk>/edit/', views.expense_update_view, name='edit'),
    path('<uuid:pk>/approve/', views.expense_approve_view, name='approve'),
]
