# Generated by Django 4.2.3 on 2023-09-21 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_cancha_news_reserva_delete_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='image',
        ),
        migrations.AddField(
            model_name='news',
            name='image_url',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
