# Generated by Django 5.1.6 on 2025-02-11 17:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_location', models.CharField(max_length=255)),
                ('dropoff_location', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('REQUESTED', 'Requested'), ('ACCEPTED', 'Accepted'), ('IN_TRANSIT', 'In Transit'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')], default='REQUESTED', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('current_location_lat', models.FloatField(null=True)),
                ('current_location_lon', models.FloatField(null=True)),
                ('estimated_pickup_time', models.DateTimeField(null=True)),
                ('actual_pickup_time', models.DateTimeField(null=True)),
                ('completed_at', models.DateTimeField(null=True)),
                ('driver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rides_as_driver', to=settings.AUTH_USER_MODEL)),
                ('rider', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rides_as_rider', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
