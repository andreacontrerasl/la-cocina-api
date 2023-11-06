from django.contrib import admin
from .models import Producto, Order, OrderItem, Categoria

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Order)
admin.site.register(OrderItem)