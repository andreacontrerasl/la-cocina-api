# Generated by Django 4.2.3 on 2023-10-05 14:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_reserva_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='news',
            name='writen_by',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='reserva',
            name='payment_code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='reserva',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('zelle', 'Zelle'), ('pago_movil', 'Pago Movil'), ('cash', 'Cash')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='reserva',
            name='payment_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='image_url',
            field=models.CharField(blank=True, max_length=400),
        ),
    ]