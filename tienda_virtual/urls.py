from django.urls import path
from . import views

urlpatterns = [
    # URLs para productos
    path('products/', views.getProducts, name='get-products'),
    path('products/create/', views.create_producto, name='create-product'),
    path('products/<int:product_id>/', views.update_producto, name='update-product'),
    path('products/<int:product_id>/delete/', views.delete_producto, name='delete-product'),

    # URLs para órdenes
    path('orders/', views.getOrders, name='get-orders'),
    path('orders/create/', views.create_order, name='create-order'),
    path('orders/<int:order_id>/', views.update_order, name='update-order'),

]
