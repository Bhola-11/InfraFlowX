from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('degradation/', views.degradation_analytics_view, name='degradation'),
    path('search/', views.global_search_view, name='global_search'),
]
