from django.urls import path
from . import views

app_name = 'conditions'

urlpatterns = [
    path('', views.condition_list_view, name='list'),
    path('create/', views.condition_log_create_view, name='create'),
    path('curves/', views.deterioration_curves_view, name='curves'),
]
