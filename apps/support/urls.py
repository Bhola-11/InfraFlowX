from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('', views.ticket_list_view, name='ticket_list'),
    path('sla/', views.sla_policy_list_view, name='sla_list'),
    path('create/', views.ticket_create_view, name='ticket_create'),
    path('<uuid:pk>/', views.ticket_detail_view, name='ticket_detail'),
    path('<uuid:pk>/edit/', views.ticket_update_view, name='ticket_edit'),
    path('<uuid:pk>/comment/', views.ticket_comment_create_view, name='ticket_comment'),
    path('<uuid:pk>/feedback/', views.ticket_feedback_create_view, name='ticket_feedback'),
]
