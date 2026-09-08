from django.urls import path
from . import views

app_name = 'contractors'

urlpatterns = [
    path('', views.contractor_list_view, name='list'),
    path('', views.contractor_list_view, name='contractor_list'),
    path('create/', views.contractor_create_view, name='create'),
    path('create/', views.contractor_create_view, name='contractor_create'),
    path('<uuid:pk>/', views.contractor_detail_view, name='detail'),
    path('<uuid:pk>/', views.contractor_detail_view, name='contractor_detail'),
    path('<uuid:pk>/edit/', views.contractor_update_view, name='edit'),
    path('<uuid:pk>/edit/', views.contractor_update_view, name='contractor_edit'),
    path('<uuid:contractor_pk>/add-agreement/', views.contract_agreement_create_view, name='add_agreement'),
    path('<uuid:contractor_pk>/add-agreement/', views.contract_agreement_create_view, name='agreement_create'),
    path('agreements/', views.contractor_list_view, name='agreement_list'),
    path('agreements/<uuid:pk>/edit/', views.contractor_update_view, name='agreement_edit'),
    path('<uuid:contractor_pk>/evaluate/', views.contractor_evaluation_create_view, name='evaluate'),
    path('<uuid:contractor_pk>/evaluate/', views.contractor_evaluation_create_view, name='evaluation_create'),
    path('evaluations/', views.contractor_list_view, name='evaluation_list'),
]
