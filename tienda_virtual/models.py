from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User  
import json

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='fotos_productos/')

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tallas = models.TextField(blank=True, default=json.dumps([]))  # Almacenar tallas como JSON
    foto = models.ImageField(upload_to='fotos_productos/')
    categoria = models.ForeignKey(Categoria, related_name='productos', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if isinstance(self.tallas, list):  # Convertir la lista a JSON antes de guardar
            self.tallas = json.dumps(self.tallas)
        super().save(*args, **kwargs)

    def get_tallas_as_list(self):
        return json.loads(self.tallas)

class Order(models.Model):
    RECEIVED = 'Received'
    PAID = 'Paid'
    SHIPPED = 'Shipped'
    CANCELED = 'Canceled'
    
    STATUS_CHOICES = [
        (RECEIVED, 'Received'),
        (PAID, 'Paid'),
        (SHIPPED, 'Shipped'),
        (CANCELED, 'Canceled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('Producto', through='OrderItem')
    shipping_address = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=RECEIVED)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('Producto', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=10, blank=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
