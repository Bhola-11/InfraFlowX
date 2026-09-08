from django.urls import path
from . import views

app_name = 'permissions'

urlpatterns = [
    path('matrix/', views.permission_matrix_view, name='matrix'),
]
