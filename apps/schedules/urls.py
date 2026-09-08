from django.urls import path
from . import views

app_name = 'schedules'

urlpatterns = [
    path('', views.schedule_list_view, name='schedule_list'),
    path('calendar/', views.schedule_calendar_view, name='calendar'),
    path('create/', views.schedule_create_view, name='schedule_create'),
    path('<uuid:pk>/', views.schedule_detail_view, name='schedule_detail'),
    path('<uuid:pk>/edit/', views.schedule_update_view, name='schedule_edit'),
    path('executions/<uuid:pk>/edit/', views.execution_update_view, name='execution_edit'),
]
