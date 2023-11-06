from django.contrib import admin

# Register your models here.

from .models import News, Cancha, Reserva


admin.site.register(News)
admin.site.register(Cancha)
admin.site.register(Reserva)

