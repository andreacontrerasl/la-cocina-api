from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime, timedelta


# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=400, default='')
    body = models.TextField()
    preview = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=True)
    image_url = models.CharField(max_length=400, blank=True)
    writen_by = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(default=timezone.now)

class Cancha(models.Model):
    nombre = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    
class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE)
    dia = models.DateField()
    hora = models.TimeField()
    
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('CANCELED', 'Canceled'),
        ('CHECK', 'Check'),
        ('PAST', 'Past'),
    )
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    
    PAYMENT_METHOD = (
        ('zelle', 'Zelle'),
        ('pago_movil', 'Pago Movil'),
        ('cash', 'Cash'),
    )
    
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, null=True, blank=True)
    
    payment_name = models.CharField(max_length=255, null=True, blank=True)
    
    payment_code = models.CharField(max_length=255, null=True, blank=True)
    
    def update_status(self):
        
        if self.status == 'CHECK' or self.status == 'CANCELED':
            return

        # Obtener la fecha y hora actual y la fecha y hora de la reserva en la misma zona horaria
        current_datetime = timezone.make_aware(timezone.datetime.now())
        print(current_datetime)
        reservation_datetime = timezone.make_aware(timezone.datetime(self.dia.year, self.dia.month, self.dia.day, self.hora.hour, self.hora.minute))
        print(reservation_datetime)
        if current_datetime < reservation_datetime:
            # La reserva todavía no ha llegado, mantenla como 'ACTIVE'
            self.status = 'ACTIVE'
        elif current_datetime < reservation_datetime + timedelta(hours=2):
            # La reserva ha pasado, pero menos de 1 hora y 30 minutos después de la hora programada,
            # no se marca como 'PAST' todavía.
            pass
        else:
            # Han pasado más de 1 hora y 30 minutos desde la hora de la reserva y no se ha marcado como 'CHECK'
            # ni 'CANCELED', así que cambiamos automáticamente a 'PAST'.
            if self.status != 'CHECK' or self.status != 'CANCELED':
                self.status = 'PAST'

    def save(self, *args, **kwargs):
        self.update_status()
        super(Reserva, self).save(*args, **kwargs)

@receiver(pre_save, sender=Reserva)
def update_reserva_status(sender, instance, **kwargs):
    instance.update_status()