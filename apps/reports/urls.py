from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_catalog_view, name='catalog'),
    path('generate/<str:code>/', views.report_generate_view, name='generate'),
    path('history/', views.generated_reports_history_view, name='history'),
]
