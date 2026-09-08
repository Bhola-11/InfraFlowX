from django.urls import path
from . import views

app_name = 'contractors'

urlpatterns = [
    path('', views.contractor_list_view, name='list'),
    path('create/', views.contractor_create_view, name='create'),
    path('<uuid:pk>/', views.contractor_detail_view, name='detail'),
    path('<uuid:pk>/edit/', views.contractor_update_view, name='edit'),
    path('<uuid:contractor_pk>/add-agreement/', views.contract_agreement_create_view, name='add_agreement'),
    path('<uuid:contractor_pk>/evaluate/', views.contractor_evaluation_create_view, name='evaluate'),
]
