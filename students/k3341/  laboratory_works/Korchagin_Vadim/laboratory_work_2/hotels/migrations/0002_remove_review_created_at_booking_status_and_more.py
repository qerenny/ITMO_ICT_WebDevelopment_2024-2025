# Generated by Django 5.1.2 on 2024-10-26 12:39

import django.core.validators
import hotels.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='created_at',
        ),
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='guest',
            name='is_primary_guest',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='guest',
            name='special_requests',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='end_date',
            field=models.DateField(validators=[hotels.models.validate_future_date]),
        ),
        migrations.AlterField(
            model_name='booking',
            name='start_date',
            field=models.DateField(validators=[hotels.models.validate_future_date]),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='Rating must be at least 1'), django.core.validators.MaxValueValidator(10, message='Rating cannot exceed 10')]),
        ),
        migrations.AlterField(
            model_name='room',
            name='capacity',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='room',
            name='cost_per_night',
            field=models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]