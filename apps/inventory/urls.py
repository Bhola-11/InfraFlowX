from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # Warehouses
    path('warehouses/', views.warehouse_list_view, name='warehouse_list'),
    path('warehouses/create/', views.warehouse_create_view, name='warehouse_create'),
    path('warehouses/<uuid:pk>/', views.warehouse_detail_view, name='warehouse_detail'),
    path('warehouses/<uuid:pk>/edit/', views.warehouse_update_view, name='warehouse_edit'),

    # Spare Parts
    path('parts/', views.sparepart_list_view, name='sparepart_list'),
    path('parts/create/', views.sparepart_create_view, name='sparepart_create'),
    path('parts/<uuid:pk>/', views.sparepart_detail_view, name='sparepart_detail'),
    path('parts/<uuid:pk>/edit/', views.sparepart_update_view, name='sparepart_edit'),

    # Stock Movements
    path('movements/', views.stock_movement_list_view, name='movement_list'),
    path('movements/create/', views.stock_movement_create_view, name='movement_create'),

    # Purchase Requisitions
    path('requisitions/', views.purchase_requisition_list_view, name='pr_list'),
    path('requisitions/create/', views.purchase_requisition_create_view, name='pr_create'),
    path('requisitions/<uuid:pk>/', views.purchase_requisition_detail_view, name='pr_detail'),
    path('requisitions/<uuid:pk>/edit/', views.purchase_requisition_update_view, name='pr_edit'),
    path('requisitions/<uuid:pk>/add-item/', views.purchase_requisition_item_create_view, name='pr_add_item'),

    # Categories
    path('categories/', views.inventory_category_list_view, name='category_list'),
]
